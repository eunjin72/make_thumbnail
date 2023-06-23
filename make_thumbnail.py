"""
makethumbnail
- You can select a frame to make a thumbnail of any size.
- This module can check video information.
"""

import os
import cv2


class MakeThumbnail:
    """
    :class: 'MakeThumbnail' makes resized a thumbnail and additional checks video information.
    """
    def __init__(self):
        """
        Attributes:
              video_path(str): video file이 있는 경로
              save_path(str): thumbnail file 저장 경로
              thumbnail(int): thumbnail로 할 frame 번호
              size(int): thumbnail의 크기 변경
        """
        self._video_path = None
        self._save_path = None
        self._thumbnail = None
        self._size = None

    @property
    def video_path(self):
        """
        video 파일의 경로를 반환한다
        """
        return self._video_path

    @video_path.setter
    def video_path(self, user_input):
        """
        video 파일이 있는 경로를 입력 받고, 파일이 있는지 확인 한다.
        """
        if os.path.isfile(user_input):
            pass
        else:
            print("The file does not exist")
        self._video_path = user_input

    @property
    def save_path(self):
        """
        thumbnail 파일을 저장할 경로를 반환 한다.
        """
        return self._save_path

    @save_path.setter
    def save_path(self, user_input):
        """
        thumbnail 파일을 저장할 폴더의 경로를 입력 받거나, 폴더가 없으면 생성 한다.
        """
        if not os.path.exists(user_input):
            os.mkdir(user_input)
        self._save_path = user_input

    @property
    def thumbnail(self):
        """
        thumbnail로 사용할 frame 번호를 반환 한다.
        """
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, user_input):
        """
        thumbnail로 사용할 frame 번호를 입력 받는다.
        """
        if self.frame < user_input:
            raise ValueError("해당 frame이 없습니다.")
        self._thumbnail = user_input

    @property
    def size(self):
        """
        thumbnail의 크기를 반환 한다.
        """
        return self._size

    @size.setter
    def size(self, user_input):
        """
        thumbnail의 절대크기로 설정한다.
        Args:
            tuple로 너비와 높이 값을 받는다.
        Raises:
            ValueError: 너비, 높이 이외 값을 받은 경우, user_input이 정수가 아니거나 0 이하인 경우
        """
        if len(user_input) >= 3:
            raise ValueError("너비, 높이 값만 입력하세요.")
        for i in user_input:
            if type(i) not in [int]:
                raise ValueError("타입을 확인해 주세요")
            if i <= 0:
                raise ValueError("타입을 확인해 주세요")
        print(type(user_input))
        self._size = user_input

    @property
    def save_frames(self):
        return self._save_frames

    @save_frames.setter
    def save_frames(self, user_input):
        self._save_frames = user_input

    def video_info(self):
        """
        vide_info 함수는 video 파일의 정보(frame, width, height, fps)를 보여 준다.
        video 파일이 있는 path를 입력하면 정보를 출력해준다.
        View video information in video_path
        """
        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():
            print("could not open :", self.video_path)
            exit(0)
        self.frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        print('frame : ', self.frame)
        print('width : ', width)
        print('height : ', height)
        print('fps : ', fps)

    def all_save_frames(self):
        # 프레임 당 이미지 저장
        cap = cv2.VideoCapture(self.video_path)
        count = 0

        while(cap.isOpened()):
            ret, image = cap.read()
            if(int(cap.get(1)) % self.save_frames == 0):
                print('Saved frame number : ' + str(int(cap.get(1))))
                cv2.imwrite(f'{self.save_path}/1%03d.jpg' % count, image)
                print('Saved 1%03d.jpg' % count)
                count += 1
            if not ret:
                break

        cap.release()

    def save_thumbnail(self):
        """
        save_thumbnail 함수는
        frame, size 값을 입력받아 thumbnail을 저장합니다.
        :return: save thumbnail
        """

        # thumbnail로 할 frame을 읽고 저장
        cap = cv2.VideoCapture(self.video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, self.thumbnail)
        res, frame = cap.read()
        cv2.imwrite(f'{self.save_path}/thumbnail_1{self.thumbnail}.jpg', frame)
        src = cv2.imread(f'{self.save_path}/thumbnail_1{self.thumbnail}.jpg', cv2.IMREAD_COLOR)

        # thumbnail size 설정
        thumbnail = cv2.resize(src, dsize=self.size, interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(f'{self.save_path}/thumbnail_1{self.thumbnail}.jpg', thumbnail)
        cv2.imshow(f'thumbnail_1{self.thumbnail}', thumbnail)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def main():
    thumb_maker = MakeThumbnail()
    thumb_maker.video_path = input("Enter video path: ")
    thumb_maker.save_path = input("Enter save path: ")

    thumb_maker.video_info()

    # 모든 frame 저장할때
    # thumb_maker.save_frames = 1
    # thumb_maker.all_save_frames()

    thumb_maker.thumbnail = int(input("select frame: "))
    thumb_maker.size = tuple(int(item) for item in input("Enter size: ").split())
    thumb_maker.save_thumbnail()


if __name__ == '__main__':
    main()
