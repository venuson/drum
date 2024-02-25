from drum_player import DrumPlayer
from section_info import SectionInfo
import pygame
import sys
import argparse


def listen_keyboard():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    print("音乐播放中，输入指令（q退出，空格开始/暂停）：")
    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.USEREVENT and event.custom_type == "STOP_PLAY":
                print("结束播放")
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print("停止播放")
                    if drum_player.is_playing():
                        drum_player.stop_play()
                        sys.exit(0)      
                if event.key == pygame.K_SPACE:
                    if drum_player.is_playing():
                        drum_player.pause_resume_play()
                        print("暂停/继续播放")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process input arguments.')
    parser.add_argument('-p', '--path', type=str, required=True, help='Input file path')
    parser.add_argument('-b', '--begin', type=int, default=0, help='Begin position')
    parser.add_argument('-s', '--speed', type=int, default=0, help='Modified speed')
    parser.add_argument('-e', '--end', type=int, default=None, help='End position')
    parser.add_argument('-r', '--repeat', type=int, default=1, help='Repeat playback times')
    parser.add_argument('-t', '--beat', action='store_true', help='Play metronome')
    args = parser.parse_args()

    if args.path is None:
        print("请指定谱信息文件")
        sys.exit(1)

    drum_player = DrumPlayer()
    drum_player.load_sheet(args.path)
    drum_player.start_play(args.begin, args.end, args.repeat, args.beat, args.speed)
    listen_keyboard()
    
