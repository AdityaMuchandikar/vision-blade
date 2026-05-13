import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, static_mode=False, max_hands=1, detection_con=0.7, track_con=0.5):
        self.static_mode = static_mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.static_mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def find_hands(self, frame, draw=True):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def get_index_tip(self, frame):
        """
        Extracts just the Index Finger Tip (Landmark 8).
        """
        index_pos = None
        if self.results and self.results.multi_hand_landmarks:
            hand_lms = self.results.multi_hand_landmarks[0]
            h, w, c = frame.shape
            
            # Landmark 8: Index Finger Tip
            index_lm = hand_lms.landmark[8]
            index_pos = (int(index_lm.x * w), int(index_lm.y * h))

        return index_pos