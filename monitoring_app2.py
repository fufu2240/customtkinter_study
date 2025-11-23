import customtkinter as ctk
from tkinter import filedialog
import threading
import cv2
from PIL import Image, ImageTk
import datetime

# AI 기능 부분 시작 (아직 안넣음) ===============================================================
class ai_simulator:
    def __init__(self):
        print("AI 모델 로드 준비 완료 (시뮬레이션 모드)")

    def check_danger(self, current_sec):
        # 시뮬레이션: 5~7초, 15~16초에 위험 감지
        if (5 < current_sec < 7) or (15 < current_sec < 16):
            return True
        return False


# GUI 부분 ===============================================================
class MonitoringApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("AI 홈카메라 모니터링 시스템")
        self.geometry("900x700")

        self.ai_simulator = ai_simulator()
        # 영상 재생/분석 상태 플래그
        self.video_running = False
        # 재생 중지 요청 플래그
        self.stop_requested = False

        # 1. 시스템의 상태를 표시하는 곳(뼈대)
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(pady=20, padx=20, fill="x")

        # 2. 시스템 상태 표시(출력)
        self.status_label = ctk.CTkLabel(
            control_frame,
            text="홈카메라 준비 완료",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="gray"
        )
        self.status_label.pack(side="left", padx=20, pady=10)

        # 3. 작동 시작/중지 버튼
        self.start_button = ctk.CTkButton(
            control_frame,
            text="작동 시작하기 (영상 선택)",
            command=self.handle_start_stop,
            font=ctk.CTkFont(size=18)
        )
        self.start_button.pack(side="right", padx=20, pady=10)

        # 4. 영상 표시 영역
        self.video_label = ctk.CTkLabel(
            self,
            text="[AI 모니터링 영상 출력]",
            width=640,
            height=480,
            fg_color=("gray80", "gray20")
        )
        self.video_label.pack(pady=10)

        # 5. 하단에 알림 로그 영역
        log_frame = ctk.CTkFrame(self)
        log_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(log_frame, text="🚨 실시간 감지 로그", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))
        self.log_textbox = ctk.CTkTextbox(log_frame, height=80)
        self.log_textbox.pack(padx=10, pady=(0, 10), fill="x")
        self.log_textbox.insert("end", f"[{self.get_time()}] 시스템 부팅 완료.\n")
        self.log_textbox.configure(state="disabled")

    # 기타 기능들
    def get_time(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def update_status(self, text, color, button_text=None, button_state="normal"):
        self.status_label.configure(text=text, text_color=color)
        if button_text:
            self.start_button.configure(text=button_text)
        self.start_button.configure(state=button_state)

    # 알림 로그 업데이트
    def add_log(self, message):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"[{self.get_time()}] {message}\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def handle_start_stop(self):
        """작동 시작/중지 버튼 클릭 핸들러"""
        if self.video_running:
            # 작동 중이면 -> 중지 요청
            self.stop_analysis()
        else:
            # 작동 중이 아니면 -> 영상 선택 및 시작
            self.select_and_start_video()

    def stop_analysis(self):
        """영상 분석 스레드를 안전하게 중지 요청"""
        if self.video_running:
            self.stop_requested = True
            # UI 상태를 '중지 요청됨'으로 즉시 변경
            self.update_status("중지 요청 중...", "darkred", "중지하는 중...", "disabled")

    def select_and_start_video(self):
        """영상 파일 선택 및 분석 스레드 시작"""
        video_path = filedialog.askopenfilename(
            title="시연 영상 파일 선택",
            filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*"))
        )

        if not video_path:
            self.update_status("홈카메라 준비 완료", "gray", "작동 시작하기 (영상 선택)", "normal")
            return

        self.update_status("작동 중...", "orange", "분석 중지하기", "normal")
        self.video_running = True
        self.stop_requested = False # 새 시작 시 플래그 초기화

        # 스레드로 영상 분석 시작
        thread = threading.Thread(target=self.run_ai_analysis, args=(video_path,))
        thread.daemon = True
        thread.start()

    def run_ai_analysis(self, video_path):
        """보조 스레드에서 실행되는 영상 분석 및 UI 업데이트 로직"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            self.after(0, lambda: self.update_status("오류: 영상 파일을 열 수 없습니다.", "red", "작동 시작하기 (영상 선택)", "normal"))
            self.video_running = False
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        delay = int(1000 / fps) if fps > 0 else 30

        try:
            while cap.isOpened() and self.video_running and not self.stop_requested:
                ret, frame = cap.read()
                if not ret:
                    break

                current_sec = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

                # --- AI 분석 로직 (시뮬레이션) ---
                is_danger = self.ai_simulator.check_danger(current_sec)

                # TODO: 여기에 실제 객체 탐지(사각형/퍼센트) 코드를 넣습니다.
                # 예: frame = draw_detection_results(frame, results)

                # GUI 업데이트 요청 (self.after(0, ...) 사용)
                self.after(0, lambda f=frame: self.update_video_frame(f))

                if is_danger:
                    # 위험 감지 시 상태 메시지 및 로그 업데이트
                    self.after(0, lambda: self.update_status("🚨 위험 감지됨! 낙상/사고 발생 🚨", "red", "분석 중지하기", "normal"))
                    # 5초/15초에 한 번만 로그를 기록하도록 플래그를 추가하는 것이 좋으나, 시연을 위해 단순화
                    self.after(0, lambda: self.add_log(f"**긴급 감지**: 낙상/이상 행동 발생 (시간: {current_sec:.2f}초)"))
                else:
                    # 정상 상태일 경우 '감지 중'으로 복구
                    self.after(0, lambda: self.update_status("감지 중...", "orange", "분석 중지하기", "normal"))

                cv2.waitKey(delay)
                
            # while 루프 종료 (영상 끝, 오류, 또는 중지 요청)

        finally:
            cap.release()
            self.video_running = False
            self.stop_requested = False
            
            # 최종 상태 업데이트
            if self.stop_requested: # 사용자가 중지 버튼을 누른 경우
                final_status_text = "사용자 요청으로 중지됨. 다시 시작 가능."
                final_color = "red"
            else: # 영상이 끝까지 재생된 경우
                final_status_text = "시연 종료. 파일 선택 후 다시 시작 가능."
                final_color = "green"
                
            self.after(0, lambda: self.update_status(final_status_text, final_color, "작동 시작하기 (영상 선택)", "normal"))

    # opencv 프레임을 라벨에 표시
    def update_video_frame(self, frame):
        """OpenCV 프레임을 CTkLabel에 표시"""
        if not self.video_running and not self.stop_requested:
            return

        try:
            # 1. 프레임 크기 조정
            frame = cv2.resize(frame, (640, 480))

            # 2. BGR을 RGB로 변환 (PIL 호환)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

            # 3. PIL Image 객체 생성
            img = Image.fromarray(cv2image)

            # 4. CustomTkinter 호환 이미지 생성
            # CTkImage는 내부적으로 PIL Image를 래핑합니다.
            img_tk = ctk.CTkImage(light_image=img, size=(640, 480))

            # 5. 라벨에 이미지 설정 및 텍스트 제거
            self.video_label.configure(image=img_tk, text="")
            # **주의**: CTkImage 객체를 self에 저장해야 가비지 컬렉션 방지
            self.video_label.image_ref = img_tk

        except Exception as e:
            # 영상이 이미 끝났거나, 중지 요청으로 인해 프레임 처리 도중 문제가 생길 수 있습니다.
            if self.video_running: # 아직 실행 중인 상태에서 에러가 발생했다면
                print(f"영상 프레임 처리 오류: {e}")
                self.stop_analysis()


# 실행
if __name__ == "__main__":
    app = MonitoringApp()
    app.mainloop()