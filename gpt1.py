#gpt로 짜봄 1
import customtkinter as ctk
from tkinter import filedialog
import threading
import cv2
from PIL import Image, ImageTk # OpenCV 이미지를 CustomTkinter에 표시하기 위해 필요

# --- AI 모델 및 로직을 모의하는 클래스 (실제 모델로 대체 예정) ---
class AISimulator:
    def __init__(self):
        # 실제 AI 모델 로드 코드 (예: self.model = tf.keras.models.load_model('your_model.h5'))
        print("AI 모델 로드 준비 완료 (시뮬레이션 모드)")

    def check_danger(self, current_sec):
        """
        AI 모델 예측을 모의하는 함수. 
        특정 시간대에 낙상이나 위험 상황이 감지된다고 가정합니다.
        """
        # 시연 영상의 5~7초와 15~16초 사이에 위험 감지 발생을 시뮬레이션
        if (5 < current_sec < 7) or (15 < current_sec < 16):
            return True
        return False
# -------------------------------------------------------------------


class MonitoringApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        self.title("AI 기반 스마트 홈 안전 모니터링 시스템 (시연)")
        self.geometry("900x700")
        
        self.ai_simulator = AISimulator()
        self.video_running = False

        # --- UI 컴포넌트 설정 ---
        
        # 1. 상태 및 제어 프레임
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(pady=20, padx=20, fill="x")

        # 2. 상태 라벨: "감지 중", "위험 감지됨"을 표시
        self.status_label = ctk.CTkLabel(
            control_frame, 
            text="시스템 준비 완료", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="gray"
        )
        self.status_label.pack(side="left", padx=20, pady=10)

        # 3. 버튼: 시연 시작/종료
        self.start_button = ctk.CTkButton(
            control_frame, 
            text="영상 파일로 시연 시작", 
            command=self.start_demo_thread,
            font=ctk.CTkFont(size=18)
        )
        self.start_button.pack(side="right", padx=20, pady=10)

        # 4. 영상 표시 영역 (640x480 해상도에 맞춤)
        self.video_label = ctk.CTkLabel(
            self, 
            text="[AI 모니터링 영상 출력]", 
            width=640, 
            height=480, 
            fg_color=("gray80", "gray20")
        )
        self.video_label.pack(pady=10)
        
        # 5. 알림 로그 영역
        log_frame = ctk.CTkFrame(self)
        log_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(log_frame, text="🚨 실시간 감지 로그", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))
        self.log_textbox = ctk.CTkTextbox(log_frame, height=80)
        self.log_textbox.pack(padx=10, pady=(0, 10), fill="x")
        self.log_textbox.insert("end", f"[{self.get_time()}] 시스템 부팅 완료.\n")
        self.log_textbox.configure(state="disabled") # 읽기 전용으로 설정

    # --- 유틸리티 함수 ---
    def get_time(self):
        """현재 시간을 'HH:MM:SS' 형식으로 반환"""
        import datetime
        return datetime.datetime.now().strftime("%H:%M:%S")

    def update_status(self, text, color, button_state="normal"):
        """메인 스레드에서 상태 라벨과 버튼 상태를 업데이트"""
        self.status_label.configure(text=text, text_color=color)
        self.start_button.configure(state=button_state)
        
    def add_log(self, message):
        """로그 텍스트 박스에 메시지를 추가"""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"[{self.get_time()}] {message}\n")
        self.log_textbox.see("end") # 스크롤을 항상 맨 아래로
        self.log_textbox.configure(state="disabled")

    # --- 스레딩 및 AI 분석 로직 ---
    def start_demo_thread(self):
        """AI 분석을 위한 백그라운드 스레드 시작"""
        if self.video_running: return

        video_path = filedialog.askopenfilename(
            title="시연 영상 파일 선택", 
            filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*"))
        )
        
        if not video_path:
            self.update_status("파일 선택 취소", "gray")
            return

        self.update_status("감지 중...", "orange", button_state="disabled")
        self.video_running = True
        
        # 백그라운드 스레드에서 영상 분석 시작
        thread = threading.Thread(target=self.run_ai_analysis, args=(video_path,))
        thread.daemon = True
        thread.start()

    def run_ai_analysis(self, video_path):
        """보조 스레드에서 실행되는 영상 분석 및 UI 업데이트 로직"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            self.after(0, lambda: self.update_status("오류: 영상 파일을 열 수 없습니다.", "red", button_state="normal"))
            self.video_running = False
            return
            
        fps = cap.get(cv2.CAP_PROP_FPS)
        delay = int(1000 / fps) if fps > 0 else 30 # 프레임 간 지연 시간 (ms)

        try:
            while cap.isOpened() and self.video_running:
                ret, frame = cap.read()
                if not ret:
                    break
                
                current_sec = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                
                # --- AI 분석 로직 (시뮬레이션) ---
                is_danger = self.ai_simulator.check_danger(current_sec)
                
                # ------------------------------
                
                # GUI 업데이트 요청 (self.after(0, ...) 사용)
                self.after(0, lambda f=frame: self.update_video_frame(f))
                
                if is_danger:
                    # 위험 감지 시 상태 메시지 및 로그 업데이트
                    self.after(0, lambda: self.update_status("🚨 위험 감지됨! 낙상/사고 발생 🚨", "red", button_state="disabled"))
                    self.after(0, lambda: self.add_log(f"**긴급 감지**: 낙상/이상 행동 발생 (시간: {current_sec:.2f}초)"))
                else:
                    # 정상 상태일 경우 '감지 중'으로 복구
                    self.after(0, lambda: self.update_status("감지 중...", "orange", button_state="disabled"))

                if cv2.waitKey(delay) & 0xFF == ord('q'):
                    break
                
        finally:
            cap.release()
            self.video_running = False
            self.after(0, lambda: self.update_status("시연 종료. 파일 선택 후 다시 시작 가능.", "green", button_state="normal"))


    def update_video_frame(self, frame):
        """OpenCV 프레임을 CTkLabel에 표시"""
        try:
            # 1. 프레임 크기 조정 (옵션)
            frame = cv2.resize(frame, (640, 480))
            
            # 2. BGR을 RGB로 변환 (PIL 호환)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            
            # 3. PIL Image 객체 생성
            img = Image.fromarray(cv2image)
            
            # 4. CustomTkinter 호환 이미지 생성
            img_tk = ctk.CTkImage(light_image=img, size=(640, 480))

            # 5. 라벨에 이미지 설정
            self.video_label.configure(image=img_tk)
            self.video_label.image = img_tk # 가비지 컬렉션 방지
            
        except Exception as e:
            print(f"영상 프레임 처리 오류: {e}")
            self.video_running = False

# --- 앱 실행 ---
if __name__ == "__main__":
    app = MonitoringApp()
    app.mainloop()