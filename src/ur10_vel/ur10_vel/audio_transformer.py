import sounddevice as sd
import numpy as np
import time
from scipy.fft import fft, fftfreq
from scipy.signal import butter, filtfilt, find_peaks, hann
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from std_msgs.msg import Float64MultiArray

import torch
import torch.nn as nn
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

import rclpy
from rclpy.node import Node
import signal
from scipy.ndimage import zoom

import os

# 参数
sample_rate = 96000  # 音频采样率
plot_duration = 15  # 秒

import scipy.io.wavfile as wav
test_wav = "/home/zzy/audio2force/data_using/audio_13.wav"
fs, sim_data = wav.read(test_wav)

class ForcePredictGRUCNN(nn.Module):
    def __init__(self, seq_len = 40, learning_rate=1e-6,):
        super().__init__()

        self.learning_rate = learning_rate
        self.seq_len = int(seq_len)
        self.criterion = nn.MSELoss()

        self.cnn2d = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=5, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.Conv2d(16, 32, kernel_size=5, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((4, 4)),  # 更保留时频结构
            nn.Flatten(),                  # → [B, 32*4*4 = 512]
        )

        self.fc = nn.Sequential(
            nn.Linear(512, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 1)
        )

        self.time_weights = nn.Parameter(torch.linspace(0.1, 1.0, int(self.seq_len)), requires_grad=True)

    def forward(self, psd_seq, speed_seq):
        psd_seq = psd_seq * self.time_weights.view(1, 1, self.seq_len, 1) 
        cnn_feat = self.cnn2d(psd_seq)
        fc = self.fc(cnn_feat)
        return fc

class ForcePredictDGRULightning(nn.Module):
    def __init__(self, input_size=5, gru_hidden_size=64, gru_num_layers=2, seq_cnn=20):
        super().__init__()

        self.criterion = nn.MSELoss()
        self.seq_len = int(seq_cnn)

        self.gru_input_size = input_size  
        self.gru = nn.GRU(self.gru_input_size, gru_hidden_size, gru_num_layers, batch_first=True)
        self.dropout = nn.Dropout(p=0.3)
        self.fc = nn.Linear(gru_hidden_size, 1)

        self.cnn2d = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((4, 4)),  # 更保留时频结构
            nn.Flatten(),                  # → [B, 32*4*4 = 512]
        )

        self.fc = nn.Sequential(
            nn.Linear(512+gru_hidden_size, 256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 1)
        )

        self.time_weights = nn.Parameter(torch.linspace(0.1, 1.0, int(self.seq_len)), requires_grad=True)

    def forward(self, psd_seq, peak_seq):
        gru_out, _ = self.gru(peak_seq)  # [B, T, H]
        psd_seq = psd_seq * self.time_weights.view(1, 1, self.seq_len, 1) 
        cnn_feat = self.cnn2d(psd_seq)
        combined_input = torch.cat([cnn_feat, gru_out[:, -1, :]], dim=-1)
        return self.fc(combined_input)
    
class ForcePredictGRU(nn.Module):

    def __init__(self, gru_hidden_size=64, gru_num_layers=2, learning_rate=1e-6, input_size=5, y_mean=0.0, y_std=1.0):
        super().__init__()
        self.learning_rate = learning_rate
        self.criterion = nn.MSELoss()

        self.gru_input_size = input_size  
        self.gru = nn.GRU(self.gru_input_size, gru_hidden_size, gru_num_layers, batch_first=True)
        # self.rnn = nn.LSTM(self.gru_input_size, gru_hidden_size, gru_num_layers, batch_first=True)
        self.dropout = nn.Dropout(p=0.3)
        self.fc = nn.Linear(gru_hidden_size, 1)
        self.max_norm_value = (0.0 - y_mean) / y_std

    def forward(self, input_seq):
        # input_seq: [B, T, 6]
        gru_out, _ = self.gru(input_seq)  # [B, T, H]
        # gru_out, _ = self.rnn(input_seq)
        dropout = self.dropout(gru_out[:, -1, :])  # use last time step
        out = self.fc(dropout)  # [B, 1]
        clamped_out = torch.clamp(out, max=self.max_norm_value)
        return clamped_out

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs  # 奈奎斯特频率
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

def match_peaks(current_freqs, current_vals, prev_freqs, feq_num, init_frequency=0.0):
    matched_freqs = []
    matched_vals = []

    # 当前帧中先取 top-N 个峰
    top_indices = np.argsort(current_vals)[-feq_num:]
    curr_top_freqs = current_freqs[top_indices]
    curr_top_vals = current_vals[top_indices]

    used = set()

    # 如果前一帧不存在，直接取当前 top-N，补齐后返回
    if prev_freqs is None:
        sorted_indices = np.argsort(curr_top_freqs)
        curr_top_freqs = curr_top_freqs[sorted_indices]
        curr_top_vals = curr_top_vals[sorted_indices]

        pad_len = feq_num - len(curr_top_freqs)
        if pad_len > 0:
            curr_top_freqs = np.pad(curr_top_freqs, (0, pad_len), constant_values=init_frequency)
            curr_top_vals = np.pad(curr_top_vals, (0, pad_len), constant_values=0.0)

        return curr_top_freqs, curr_top_vals

    # Step 1: 基于最小距离做匹配
    for prev_f in prev_freqs:
        if len(curr_top_freqs) == 0:
            matched_freqs.append(prev_f)
            matched_vals.append(0.0)
            continue

        dists = np.abs(curr_top_freqs - prev_f)
        dists[list(used)] = np.inf  # 排除已用
        min_idx = np.argmin(dists)

        if dists[min_idx] == np.inf:
            matched_freqs.append(prev_f)
            matched_vals.append(0.0)
        else:
            matched_freqs.append(curr_top_freqs[min_idx])
            matched_vals.append(curr_top_vals[min_idx])
            used.add(min_idx)

    # Step 2: 如果还不够 feq_num，就把剩下没被使用的 current_freq 拷贝进去
    for i in range(len(curr_top_freqs)):
        if len(matched_freqs) >= feq_num:
            break
        if i not in used:
            matched_freqs.append(curr_top_freqs[i])
            matched_vals.append(curr_top_vals[i])

    # Step 3: 还不够就补默认值
    while len(matched_freqs) < feq_num:
        matched_freqs.append(init_frequency)
        matched_vals.append(0.0)

    return np.array(matched_freqs), np.array(matched_vals)

class AudioTransformer(Node):
    def __init__(self):
        super().__init__("audio_transformer")

        # 初始化网络
        self.GRU_initializer()

        self.segments = []  # 存储音频片段
        self.data_list = []  # 用于显示最近几秒的数据
        self.seq_buffer = []  # 存储GRU网络预测序列
        self.log_psd_buffer = []  # 存储CNN对数功率谱密度
        self.prev_top3_freq = None  # 记录上一帧的3个峰值频率
        self.y_pred = 0.0  # 网络预测值
        self.eef_vel = np.zeros(6)  # 机械臂末端速度
        self.running = True  # 用于控制节点是否运行
        self.sim_audio_flag = 50   # 用于记录仿真读取的位置

        # 读取滤波器参数
        stats = np.load('/home/zzy/audio2force/data_using/filt_stats.npz')
        self.lowcut = stats['lowcut']
        self.highcut = stats['highcut']
        segment_duration = stats['segment_duration']
        self.peak_freqs_high_limit = stats['peak_freqs_high_limit']
        self.peak_freqs_low_limit = stats['peak_freqs_low_limit']
        self.init_fequency = stats['init_fequency']
        self.psd_dim = stats['psd_dim']
        self.feq_num = stats['feq_num']
        overlap = stats['overlap']

        # 初始化图像
        self.psd_plot = np.zeros((self.psd_dim, 1))
        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        self.im = self.ax.imshow(np.zeros((self.psd_dim, 1)),
                                 aspect='auto', origin='lower', cmap='viridis')
        self.cbar = self.fig.colorbar(self.im, ax=self.ax)
        self.ax.set_xlabel("Time step")
        self.ax.set_ylabel("Frequency bin")
        self.ax.set_title("PSD over Time")
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=200)

        # 创建发布者
        self.publisher_force_predict = self.create_publisher(Float64MultiArray, "force_predict", 1)

        # 创建订阅者
        self.eef_vel_subscription = self.create_subscription(
            Float64MultiArray,
            '/eef_vel',
            self.eef_vel_callback,
            10)
        self.eef_vel_subscription

        self.segment_samples = int(sample_rate * segment_duration)
        self.hop_samples = int(self.segment_samples * (1 - overlap))
        self.overlap_samples = int(self.segment_samples * overlap)
        self.buffer = np.zeros((0,))
        
        # 开始录音，回调实时执行
        self.stream = sd.InputStream(
            callback=self.audio_callback,
            channels=1,
            samplerate=sample_rate,
            blocksize=self.hop_samples  # 每次采集 hop_size 大小
        )
        self.stream.start()

        self.get_logger().info('start audio recording')

    def update_plot(self, frame):
        # 更新图像
        self.im.set_data(self.psd_plot)
        self.im.set_extent((0, self.psd_plot.shape[1], 0, self.psd_dim))
        self.im.set_clim(np.min(self.psd_plot), np.max(self.psd_plot))  # 可选自动调色

    def GRU_initializer(self):
        # 使用GPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # # 使用GRU/CNN混合网络
        # checkpoint = torch.load('/home/zzy/audio2force/data_using/force_predict_DGru.pth', map_location=self.device, weights_only=False)
        # self.seq_cnn = checkpoint['seq_cnn']
        # self.seq_gru = checkpoint['seq_gru']
        # hidden_size = checkpoint['hidden_size']
        # num_layers = checkpoint['num_layers']
        # input_size = checkpoint['input_size']
        # # 加载归一化参数
        # stats = np.load('/home/zzy/audio2force/data_using/dGru_normalization_stats.npz')
        # self.X_mean_psd = stats['X_mean_psd']
        # self.X_std_psd = stats['X_std_psd']
        # self.X_mean_vel = stats['X_mean_vel']
        # self.X_std_vel = stats['X_std_vel']
        # self.y_mean = stats['y_mean']
        # self.y_std = stats['y_std']

        # self.model = ForcePredictDGRULightning(input_size=input_size, gru_hidden_size=hidden_size, gru_num_layers=num_layers, seq_cnn=self.seq_cnn).to(self.device)
        # self.model.load_state_dict(checkpoint['model_state_dict'])
        # self.model.eval()

        # 使用CNN网络
        checkpoint = torch.load('/home/zzy/audio2force/data_using/force_predict_cnnGru.pth', map_location=self.device, weights_only=False)
        self.seq_cnn = checkpoint['seq_len']
        self.seq_gru = self.seq_cnn

        stats = np.load('/home/zzy/audio2force/data_using/cnnGru_normalization_stats.npz')
        self.X_mean_psd = stats['X_mean_psd']
        self.X_std_psd = stats['X_std_psd']
        self.X_mean_vel = stats['X_mean_vel']
        self.X_std_vel = stats['X_std_vel']
        self.y_mean = stats['y_mean']
        self.y_std = stats['y_std']

        self.model = ForcePredictGRUCNN(seq_len=self.seq_cnn).to(self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval()

        # # 使用GRU网络   
        # checkpoint = torch.load('/home/zzy/audio2force/data_using/force_predict_gru.pth', map_location=self.device, weights_only=False)
        # self.seq_gru = checkpoint['seq_len']
        # self.seq_cnn = self.seq_gru
        # hidden_size = checkpoint['hidden_size']
        # num_layers = checkpoint['num_layers']
        # input_size = checkpoint['input_size']

        # stats = np.load('/home/zzy/audio2force/data_using/gru_normalization_stats.npz')
        # self.X_mean_vel = stats['X_mean']
        # self.X_std_vel = stats['X_std']
        # self.y_mean = stats['y_mean']
        # self.y_std = stats['y_std']

        # self.model = ForcePredictGRU(gru_hidden_size=hidden_size, gru_num_layers=num_layers, input_size=input_size, y_mean=self.y_mean, y_std=self.y_std).to(self.device)
        # self.model.load_state_dict(checkpoint['model_state_dict'])
        # self.model.eval()

    def predict(self, X_psd, X_vel):
        self.model.eval()  # 切换到评估模式

        sample_psd_tensor = torch.tensor(X_psd, dtype=torch.float32).to(self.device)
        sample_vel_tensor = torch.tensor(X_vel, dtype=torch.float32).to(self.device)

        with torch.no_grad():
            y_pred = self.model(sample_psd_tensor, sample_vel_tensor).cpu().numpy()  # 预测结果
            # y_pred = self.model(sample_psd_tensor).cpu().numpy()  # 预测结果

        return y_pred

    def normalize_data_and_predict(self, X_seq, v_seq):
        # 输入标准化
        # X_seq_norm = 0.0
        # X_seq_norm = (X_seq - self.X_mean_psd) / self.X_std_psd
        X_seq_norm = X_seq * 10
        v_seq_norm = 0.0
        # v_seq_norm = (v_seq - self.X_mean_vel) / self.X_std_vel

        y_pred_norm = self.predict(X_seq_norm, v_seq_norm)

        # 输出反标准化
        y_pred = y_pred_norm * self.y_std + self.y_mean
        return y_pred
    
    def update_sequence_buffer(self, log_psd, new_input):
        buffer_ready = False
        self.seq_buffer.append(new_input)
        self.log_psd_buffer.append(log_psd)

        # 超过长度就移除最早的数据
        if len(self.seq_buffer) > self.seq_cnn:
            self.seq_buffer.pop(0)
            self.log_psd_buffer.pop(0)

        # 如果长度够就返回序列
        if len(self.seq_buffer) == self.seq_cnn:
            buffer_ready = True
            return buffer_ready  # shape = (1, seq_len, input_dim)
        else:
            return buffer_ready

    # def update_plot(self,frame):

    #     if self.data_list:
    #         # 更新折线图
    #         times, values = zip(*self.data_list)
    #         times = [t - times[0] for t in times]
    #         self.line.set_data(times, values)
    #         self.ax.set_xlim(0, plot_duration)
    #         # 自动调整y轴范围
    #         self.ax.relim()  # 重新计算数据范围
    #         self.ax.autoscale_view()  # 自动缩放视图

    #     return self.line

    def save_all_data(self):
        audio_file_path = '/home/zzy/temporary_data/audio_data.wav'

        if len(self.segments) == 0:
            self.get_logger().info("No audio data to save.")
            return

        segment = np.concatenate(self.segments, axis=0)
        wav.write(audio_file_path, sample_rate, (segment * 32767).astype(np.int16))
        self.get_logger().info(f"Saved audio to: {audio_file_path}")

    def eef_vel_callback(self, msg):
        self.eef_vel = msg.data

    def audio_callback(self, indata, frames, info, status):

        if status:
            print(status)

        if indata.shape[1] > 1:
            audio = indata.mean(axis=1)  # 多声道取平均转单声道
        else:
            audio = indata[:, 0]         # 单声道直接取第一列

        audio = sim_data[self.sim_audio_flag : self.sim_audio_flag + self.hop_samples]
        self.sim_audio_flag += self.hop_samples

        # 把新数据拼接到 buffer 上
        self.buffer = np.concatenate([self.buffer, audio])

        if len(self.buffer) >= self.segment_samples:
            segment = self.buffer[-self.segment_samples:]
            self.buffer = self.buffer[-self.overlap_samples:]

            filtered_segment = bandpass_filter(segment, self.lowcut, self.highcut, sample_rate)

            window = hann(len(filtered_segment))
            windowed_segment = filtered_segment * window

            N = len(windowed_segment)
            # N = len(filtered_segment)
            T = 1.0 / sample_rate
            yf = fft(windowed_segment)
            # yf = fft(filtered_segment)
            xf = fftfreq(N, T)[:N // 2]
            psd = (1.0 / (sample_rate * N)) * (np.abs(yf[:N // 2]) ** 2) * 2

            # Step 3: limit frequency band (只保留目标频段）
            freq_mask = (xf >= self.peak_freqs_low_limit) & (xf <= self.peak_freqs_high_limit)
            xf_limited = xf[freq_mask]
            psd_limited = psd[freq_mask]

            # # log 变换
            # min_psd_value = 1e-3  # 抬高到底噪能量水平，与另一个程序对齐
            # log_psd_limited = np.log(psd_limited)
            log_psd_limited = psd_limited / (np.max(psd_limited) + 1e-8)

            # 重采样
            x_old = np.linspace(0, 1, log_psd_limited.shape[0])
            x_new = np.linspace(0, 1, self.psd_dim)
            log_psd = np.interp(x_new, x_old, log_psd_limited)

            # 找峰值
            peaks, _ = find_peaks(psd)
            peak_freqs = xf[peaks]
            peak_vals = psd[peaks]

            # 限制最大频率范围内的峰值索引
            valid_idx = np.where((peak_freqs >= self.peak_freqs_low_limit) & (peak_freqs <= self.peak_freqs_high_limit))[0]

            # 取有效峰值和频率
            valid_peak_vals = peak_vals[valid_idx]
            valid_peak_freqs = peak_freqs[valid_idx]

            if len(valid_peak_vals) == 0:
                top3_freq = np.array([self.init_fequency] * self.feq_num)
                top3_val = np.array([0.0] * self.feq_num)

            else:
                top3_freq, top3_val = match_peaks(valid_peak_freqs, valid_peak_vals, self.prev_top3_freq, feq_num=self.feq_num, init_frequency=self.init_fequency)

            # 保存当前帧峰值，供下一帧使用
            self.prev_top3_freq = top3_freq.copy()

            # 拼接成输入特征矩阵
            freq_amp_pair = np.column_stack((top3_freq, top3_val)).flatten()
            new_input_features = np.hstack([freq_amp_pair, self.eef_vel[2]])

            ready_sign = self.update_sequence_buffer(log_psd, new_input_features)
            # 如果序列已经达到预测长度
            if ready_sign:
                X_seq = np.array(self.seq_buffer[-self.seq_gru:])
                psd_list = np.vstack(self.log_psd_buffer)
                self.psd_plot = psd_list.T
                # # 重采样以统一PSD维度
                # if psd_list.shape[1] != self.psd_dim:
                #     zoom_factor = self.psd_dim / psd_list.shape[1]
                #     psd_zoom = zoom(psd_list, (1, zoom_factor))

                self.y_pred = self.normalize_data_and_predict(psd_list, X_seq)
                # 发布预测值
                msg = Float64MultiArray()
                msg.data = self.y_pred[0].tolist()
                self.publisher_force_predict.publish(msg)

            # 记录时间和频率和音频片段
            current_time = time.time()
            # self.data_list.append((current_time, top_freq))  
            self.segments.append(audio.copy())

            # 清除超过5秒的数据
            self.data_list = [(t, data) for t, data in self.data_list if current_time - t <= plot_duration]

    def shutdown(self):
        # 保存音频数据
        self.save_all_data()

        # 停止音频流
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()

        self.running = False

def main(args=None):

    rclpy.init(args=args)
    audio_transformer = AudioTransformer()

    def shutdown_handler(signum, frame):
        audio_transformer.shutdown()

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        while rclpy.ok() and audio_transformer.running:
            rclpy.spin_once(audio_transformer, timeout_sec=1)
            plt.pause(0.01)

    finally:
        audio_transformer.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()



