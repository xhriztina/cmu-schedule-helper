#!/usr/bin/env python3
"""
Parse CMU's "Full Schedule Of Classes" HTML export into courses.json.

Usage:
    python3 parse_schedule.py <input.html> [output.json]

The input HTML file can be downloaded from:
    https://enr-apps.as.cmu.edu/open/SOC/SOCServlet/completeSchedule

If no output path is given, writes to data/courses.json.
"""

import json
import re
import sys
from html.parser import HTMLParser
from datetime import datetime


class CMUScheduleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.courses = []
        self.current_department = None
        self.in_td = False
        self.in_bold = False
        self.current_row = []
        self.current_cell = ""
        self.current_course = None

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.current_row = []
        elif tag == 'td':
            self.in_td = True
            self.current_cell = ""
        elif tag == 'b':
            self.in_bold = True

    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td = False
            self.current_row.append(self.current_cell.strip())
        elif tag == 'b':
            self.in_bold = False
        elif tag == 'tr':
            self._process_row(self.current_row)

    def handle_data(self, data):
        if self.in_td:
            self.current_cell += data

    def _process_row(self, cells):
        if not cells:
            return
        first = cells[0] if cells else ""

        # Department header: text in first cell, rest empty
        if (len(cells) >= 5 and first and first != '\xa0' and first != ''
                and all(c in ('', '\xa0', ' ') for c in cells[1:])
                and not re.match(r'^\d{5}$', first)
                and first not in ('Course',)):
            self.current_department = first
            return

        if first == 'Course':
            return

        # Course row: 5-digit number
        if re.match(r'^\d{5}$', first) and len(cells) >= 7:
            course_num = first
            title = cells[1] if cells[1] != '\xa0' else ""
            units = cells[2] if cells[2] != '\xa0' else ""
            sec = cells[3] if len(cells) > 3 and cells[3] != '\xa0' else ""
            days = cells[4] if len(cells) > 4 and cells[4] != '\xa0' else ""
            begin = cells[5] if len(cells) > 5 and cells[5] != '\xa0' else ""
            end = cells[6] if len(cells) > 6 and cells[6] != '\xa0' else ""

            dept_code = course_num[:2]
            course_level = int(course_num[2]) * 100

            self.current_course = {
                "num": f"{dept_code}-{course_num[2:]}",
                "dept": dept_code,
                "level": course_level,
                "title": title,
                "units": units,
                "deptName": self.current_department or "",
                "sections": []
            }
            self.current_course["sections"].append({
                "id": sec, "days": days, "begin": begin, "end": end
            })
            self.courses.append(self.current_course)

        # Continuation row (additional section or title text)
        elif self.current_course and (first == '' or first == '\xa0'):
            title_text = cells[1] if len(cells) > 1 and cells[1] != '\xa0' else ""
            sec = cells[3] if len(cells) > 3 and cells[3] != '\xa0' else ""
            days = cells[4] if len(cells) > 4 and cells[4] != '\xa0' else ""
            begin = cells[5] if len(cells) > 5 and cells[5] != '\xa0' else ""
            end = cells[6] if len(cells) > 6 and cells[6] != '\xa0' else ""

            if sec or days:
                self.current_course["sections"].append({
                    "id": sec, "days": days, "begin": begin, "end": end
                })
            if title_text and not sec and not days:
                if self.current_course["title"]:
                    self.current_course["title"] += " " + title_text
                else:
                    self.current_course["title"] = title_text


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "data/courses.json"

    print(f"Reading: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Fix malformed rows (some <TR> tags missing)
    html = re.sub(r'\n<TD', '\n<TR><TD', html)
    html = re.sub(r'<TR><TR>', '<TR>', html)

    # Extract semester info
    sem_match = re.search(r'Semester:\s*(.+?)</B>', html)
    semester = sem_match.group(1).strip() if sem_match else "Unknown"

    date_match = re.search(r'Run Date:\s*(.+?)[\n<]', html)
    run_date = date_match.group(1).strip() if date_match else datetime.now().strftime('%Y-%m-%d')

    parser = CMUScheduleParser()
    parser.feed(html)

    output = {
        "semester": semester,
        "updated": run_date,
        "courses": parser.courses
    }

    with open(output_path, "w") as f:
        json.dump(output, f, separators=(',', ':'))

    size_kb = len(json.dumps(output, separators=(',', ':'))) / 1024
    print(f"Semester: {semester}")
    print(f"Courses:  {len(parser.courses)}")
    print(f"Output:   {output_path} ({size_kb:.0f}KB)")
    print("Done!")


if __name__ == '__main__':
    main()
