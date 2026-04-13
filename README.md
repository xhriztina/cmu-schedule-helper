# CMU Schedule Helper

Interactive tool to filter CMU courses by degree requirements, department, level, and schedule conflicts.

**[Live Demo →](https://xhriztina.github.io/cmu-schedule-helper/)**

## Features

- Filter by **custom requirement configs** (CIT Elective, General Technical, or your own)
- Block time slots manually or **import .ics calendar files**
- Filter by department, course level, and text search
- Shareable configs — anyone can create and load their own requirement definitions
- Requirement editor built in — create/edit configs right in the browser
- Shows which sections conflict with your schedule

## Quick Start

1. Clone this repo
2. Enable GitHub Pages (Settings → Pages → Source: main branch)
3. Visit `https://xhriztina.github.io/cmu-schedule-helper/`

## Updating for a New Semester

1. Go to [CMU Schedule of Classes](https://enr-apps.as.cmu.edu/open/SOC/SOCServlet/completeSchedule)
2. Download the full schedule HTML page (Ctrl+S / Cmd+S)
3. Run the parser:
   ```bash
   python3 tools/parse_schedule.py "Carnegie_Mellon_University_-_Full_Schedule_Of_Classes.html" data/courses.json
   ```
4. Commit and push — the site updates automatically

## Requirement Configs

Configs live in `configs/` as JSON files. The app ships with `ece-ms.json` as an example.

### Config Format

```json
{
  "id": "your-program",
  "name": "Your Program Name",
  "description": "Brief description of this requirement set.",
  "categories": [
    {
      "id": "category-id",
      "name": "Display Name",
      "description": "What this requirement is for.",
      "color": "#60a5fa",
      "minLevel": 600,
      "departments": ["18", "15", "16"],
      "includeCourses": ["51-882", "99-783"],
      "excludeCourses": ["19-602"],
      "notes": "Optional notes shown in the UI."
    }
  ]
}
```

### Fields

| Field | Description |
|-------|-------------|
| `departments` | Array of 2-digit department codes whose courses qualify |
| `minLevel` | Minimum course number level (e.g. 600 for graduate) |
| `includeCourses` | Specific courses that qualify regardless of department |
| `excludeCourses` | Specific courses that do NOT qualify even if dept matches |
| `color` | Hex color for the requirement badge in the UI |

### Creating Your Own

1. Copy `configs/ece-ms.json` as a starting point
2. Edit the categories to match your program's requirements
3. Add the file to `configs/` and commit
4. In the app, click "Load Config" and select your file
5. Or use the built-in requirement editor to create configs in the browser and export them

### Sharing Configs

You can share configs by:
- Adding them to the `configs/` folder in the repo
- Pasting the JSON URL into the app's "Load Config from URL" input
- Exporting from the editor and sending the JSON file directly

## File Structure

```
├── index.html              # The app (single page, no build step)
├── data/
│   └── courses.json        # Parsed course data
├── configs/
│   └── ece-ms.json          # Example requirement config
├── tools/
│   └── parse_schedule.py    # HTML → courses.json converter
└── README.md
```

## Department Codes

| Code | Department |
|------|-----------|
| 02 | Computational Biology |
| 03 | Biological Sciences |
| 04 | CMU-Africa / ICT |
| 05 | Human-Computer Interaction |
| 06 | Chemical Engineering |
| 08 | Institute for Software Research |
| 09 | Chemistry |
| 10 | Machine Learning |
| 11 | Language Technologies |
| 12 | Civil & Environmental Engineering |
| 14 | Information Networking Institute |
| 15 | Computer Science |
| 16 | Robotics |
| 17 | Software & Societal Systems |
| 18 | Electrical & Computer Engineering |
| 19 | Engineering & Public Policy |
| 21 | Mathematical Sciences |
| 24 | Mechanical Engineering |
| 27 | Materials Science & Engineering |
| 33 | Physics |
| 36 | Statistics & Data Science |
| 39 | CIT Interdisciplinary |
| 42 | Biomedical Engineering |
| 45 | Business Administration (Tepper) |
| 49 | Integrated Innovation Institute |
| 53 | Entertainment Technology Center |
| 86 | Neuroscience Institute |
| 94 | Heinz College Wide |
| 95 | Information Systems (Heinz) |
