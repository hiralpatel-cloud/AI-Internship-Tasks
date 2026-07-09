# Student Performance Prediction System

## Project Overview
This project is a Machine Learning application developed using Python and Scikit-learn. It predicts whether a student will **Pass** or **Fail** based on the following input features:

- Study Hours
- Attendance (%)
- Assignment Marks

The model is trained using the Logistic Regression algorithm and provides predictions based on user input.

---

## Features
- Load student dataset from a CSV file
- Check for missing values
- Split dataset into training and testing sets
- Train a Logistic Regression model
- Evaluate model accuracy
- Save the trained model
- Predict student performance using user input

---

## Technologies Used
- Python
- Pandas
- Scikit-learn
- Joblib

---

## Project Structure

```
Mini_Project/
│
├── dataset/
│   └── student_data.csv
│
├── models/
│
├── student_performance_prediction.py
│
└── README.md
```

---

## Dataset

The dataset contains the following columns:

| Column | Description |
|---------|-------------|
| StudyHours | Number of study hours |
| Attendance | Attendance percentage |
| Assignments | Assignment marks |
| Pass | 1 = Pass, 0 = Fail |

---

## How to Run

1. Open the project folder.
2. Activate the virtual environment.
3. Run the program:

```bash
python student_performance_prediction.py
```

4. Enter:
   - Study Hours
   - Attendance
   - Assignment Marks

5. The program predicts whether the student will **Pass** or **Fail**.

---

## Example

**Input**

```
Study Hours: 8
Attendance: 90
Assignment Marks: 85
```

**Output**

```
Prediction: PASS
```

---

## Future Improvements

- Add a graphical user interface (GUI)
- Use a larger real-world student dataset
- Compare multiple machine learning models
- Deploy the project as a web application

---

## Author

**Hiral Barsaniya**