
// API URL
const API_URL = "/api/students";

// Get HTML elements
const studentForm = document.getElementById("studentForm");
const studentTable = document.getElementById("studentTable");
const studentId = document.getElementById("studentId");
const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const courseInput = document.getElementById("course");
const submitBtn = document.getElementById("submitBtn");
const cancelBtn = document.getElementById("cancelBtn");
const searchInput = document.getElementById("searchInput");
const message = document.getElementById("message");

let students = [];


// Display messages
function showMessage(text, isError = false) {
    message.textContent = text;
    message.style.color = isError ? "#dc2626" : "#15803d";
}


// Reset form
function resetForm() {
    studentForm.reset();
    studentId.value = "";
    submitBtn.textContent = "Add Student";
    cancelBtn.hidden = true;
    document.getElementById("formTitle").textContent =
        "Add New Student";
}


// GET - Load students
async function loadStudents() {

    try {
        const response = await fetch(API_URL);
        const data = await response.json();

        if (!response.ok) {
            throw new Error("Unable to load students.");
        }

        students = data.students;
        displayStudents(students);

    } catch (error) {
        showMessage(error.message, true);
    }
}


// Display students in table
function displayStudents(records) {

    studentTable.replaceChildren();

    records.forEach(student => {

        const row = document.createElement("tr");

        const values = [
            student.id,
            student.name,
            student.email,
            student.course
        ];

        values.forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });

        // Action buttons
        const actionCell = document.createElement("td");

        const editButton = document.createElement("button");
        editButton.textContent = "Edit";
        editButton.className = "edit-btn";
        editButton.addEventListener("click", () => {
            editStudent(student.id);
        });

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.className = "delete-btn";
        deleteButton.addEventListener("click", () => {
            deleteStudent(student.id);
        });

        actionCell.appendChild(editButton);
        actionCell.appendChild(deleteButton);

        row.appendChild(actionCell);
        studentTable.appendChild(row);
    });
}


// POST - Add student
// PUT - Update student
studentForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    const id = studentId.value;

    const studentData = {
        name: nameInput.value.trim(),
        email: emailInput.value.trim(),
        course: courseInput.value.trim()
    };

    const method = id ? "PUT" : "POST";

    const url = id
        ? `${API_URL}/${id}`
        : API_URL;

    try {

        const response = await fetch(url, {
            method: method,

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(studentData)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.message);
        }

        showMessage(result.message);

        resetForm();
        await loadStudents();

    } catch (error) {
        showMessage(error.message, true);
    }

});


// Fill form for editing
function editStudent(id) {

    const student = students.find(s => s.id === id);

    if (!student) return;

    studentId.value = student.id;
    nameInput.value = student.name;
    emailInput.value = student.email;
    courseInput.value = student.course;

    submitBtn.textContent = "Update Student";
    cancelBtn.hidden = false;

    document.getElementById("formTitle").textContent =
        "Edit Student";

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


// DELETE - Remove student
async function deleteStudent(id) {

    if (!confirm("Are you sure you want to delete this student?")) {
        return;
    }

    try {

        const response = await fetch(`${API_URL}/${id}`, {
            method: "DELETE"
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.message);
        }

        showMessage(result.message);

        await loadStudents();

    } catch (error) {
        showMessage(error.message, true);
    }
}


// Search students
searchInput.addEventListener("input", function() {

    const keyword = searchInput.value.toLowerCase();

    const filteredStudents = students.filter(student =>
        student.name.toLowerCase().includes(keyword) ||
        student.email.toLowerCase().includes(keyword) ||
        student.course.toLowerCase().includes(keyword)
    );

    displayStudents(filteredStudents);
});


// Cancel edit
cancelBtn.addEventListener("click", resetForm);


// Load records when page opens
loadStudents();
