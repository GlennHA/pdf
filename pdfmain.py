from dataclasses import dataclass
# from distutils.fancy_getopt import fancy_getopt
import operator
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@dataclass(order=True)
class Lektion():
    ypos: int
    lektion: list[str] = None
    indhold: list[str] = None
    arbejdsform: list[str] = None
    litteratur: list[str] = None


@dataclass
class Fag():
    lektion_x: int = -1
    indhold_x: int = -1
    arbejdsform_x:  int = -1
    litteratur_x: int = -1
    lektioner: list[Lektion] = None


@dataclass
class Textbox:
    x: int
    y: int
    txt: str
    org: LTTextBoxHorizontal
    c: dict


def main():
    lst: list[Textbox] = []
    for i, page_layout in enumerate(extract_pages('2_semester.pdf')):
        if True:  # i >= 24 and i <= 26:
            for element in page_layout:
                if isinstance(element, LTTextBoxHorizontal):
                    # print(element)
                    x = int(element.bbox[0])
                    y = int(850 - element.bbox[3] + i * 850)
                    lst.append(
                        Textbox(x, y, element.get_text().replace('\n', ''), element, {}))
    lst = [item for item in lst if 'ucsyd.dk' not in item.txt]
    lst = [item for item in lst if 'Professionsbachelor i sygepleje' not in item.txt]
    lst = sorted(lst, key=operator.attrgetter('y', 'x'))

    # fag = Fag()
    fag = None
    alt = []
    i = 0
    with open("2_semester_extract.txt", "w", encoding="UTF-8") as f:
        while i < len(lst):
            # print(i, lst[i])
            if 'LEKT' in lst[i].txt:
                fag = Fag(lst[i].x, lst[i+1].x, lst[i+2].x, lst[i+3].x, [])
                alt.append(fag)
                i += 4
                continue
            if fag is None:
                i += 1
                continue
            # if (lst[i].x == fag.lektion_x) or (i+2 < len(lst) and lst[i+2].x == fag.lektion_x):
            #     lektion = Lektion(lst[i].y, [], [], [], [])
            #     lektion.lektion.append(lst[i].txt)
            #     fag.lektioner.append(lektion)
            # if lst[i].x == fag.indhold_x:
            #     lektion.indhold.append(lst[i].txt)
            # if lst[i].x == fag.arbejdsform_x:
            #     lektion.arbejdsform.append(lst[i].txt)
            if lst[i].x == fag.litteratur_x:
                f.write(lst[i].txt + '\n')
                # lektion.litteratur.append(lst[i].txt)
            i += 1

    # for fag in alt:
    #     fag.lektioner = [
    #         lektion for lektion in fag.lektioner if len(lektion.indhold) > 0]

    # print(alt)

    # search = "undhedsfremme"
    # for fag in alt:
    #     for lektion in fag.lektioner:
    #         for item in lektion.litteratur:
    #             if search in item:
    #                 print(lektion.indhold[0], item.replace(search, bcolors.OKGREEN + search + bcolors.ENDC))

    # for fag in alt:
    #     for lektion in fag.lektioner:
    #         print("---------------")
    #         print(lektion.lektion)
    #         print(lektion.indhold)
    #         print(lektion.arbejdsform)
    #         print(lektion.litteratur)


if __name__ == '__main__':
    main()
