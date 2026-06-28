# 🤖 AgentMotion

AgentMotion is an AI-powered robotics task planner that converts natural language instructions into structured robot execution plans using Google's Gemini API.

## 🚀 Features

- 🧠 Converts natural language into robot task plans
- 🤖 Uses Google's Gemini API for intelligent planning
- 📋 Generates structured JSON output
- 🌐 Interactive web interface built with Streamlit
- 💾 Automatically saves generated plans as JSON files

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini API
- JSON
- python-dotenv
- Git & GitHub

## 📂 Project Structure

```text
AgentMotion/
│
├── app.py              # Streamlit web application
├── main.py             # Terminal version
├── outputs/            # Generated robot plans
├── .env.example        # Example environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## ▶️ Getting Started

### Clone the repository

```bash
git clone https://github.com/rinchu08/AgentMotion.git
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```text
GEMINI_API_KEY=YOUR_API_KEY
```

### Run the application

```bash
streamlit run app.py
```

## 💡 Example

### User Instruction

> Pick up the red bottle from the table and place it in the basket.

### Generated Plan

```json
{
  "task": "Move Bottle",
  "source": "Table",
  "destination": "Basket",
  "steps": [
    {
      "action": "detect_object",
      "object": "red bottle",
      "location": "table"
    },
    {
      "action": "grasp_object",
      "object": "red bottle"
    },
    {
      "action": "move_to_location",
      "location": "basket"
    },
    {
      "action": "release_object",
      "object": "red bottle"
    }
  ]
}
```

## 🚧 Roadmap

- [x] Gemini API Integration
- [x] Streamlit Web Interface
- [x] JSON Export
- [ ] Conversation History
- [x] Image Upload
- [ ] Gemini Vision Integration
- [ ] ROS2 Command Generator
- [ ] Robot Simulation
- [ ] Voice Commands

## 👨‍💻 Author

**Rinchu Thulaseedharan Sunitha**

GitHub: https://github.com/rinchu08

---

⭐ If you like this project, consider giving it a star!
