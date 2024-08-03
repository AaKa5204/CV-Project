import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=self.mode, 
                                         max_num_hands=self.max_hands, 
                                         min_detection_confidence=self.detection_confidence, 
                                         min_tracking_confidence=self.tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0, draw=True):
        lm_list = []
        if self.results.multi_hand_landmarks:
            hand_lms = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(hand_lms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lm_list

def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    
    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break
        
        img = tracker.find_hands(img)
        lm_list = tracker.find_position(img)
        
        if lm_list:
            print(lm_list[4])  # Example: Print the position of landmark 4 (thumb tip)
        
        cv2.imshow("Hand Tracking", img)
        if cv2.waitKey(1) & 0xFF == 27:  # Exit on pressing 'Esc'
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
