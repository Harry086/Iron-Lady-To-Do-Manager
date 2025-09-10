function loadTasks() {
  fetch("/tasks")
    .then(res => res.json())
    .then(tasks => {
      const list = document.getElementById("taskList");
      list.innerHTML = "";
      tasks.forEach(task => {
        const li = document.createElement("li");
        li.className = "task";
        li.innerHTML = `
          <input type="text" value="${task.title}" readonly ondblclick="this.removeAttribute('readonly')">
          <div>
            <button onclick="updateTask(${task.id}, this)">Edit</button>
            <button style="background:red" onclick="deleteTask(${task.id})">Delete</button>
          </div>
        `;
        list.appendChild(li);
      });
    });
}

function addTask() {
  const input = document.getElementById("taskInput");
  const title = input.value.trim();
  if (!title) return;

  fetch("/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title })
  })
  .then(res => res.json())
  .then(() => {
    input.value = "";
    loadTasks();
  });
}

function updateTask(id, btn) {
  const input = btn.parentElement.parentElement.querySelector("input");
  const isReadonly = input.hasAttribute("readonly");

  if (isReadonly) {
    input.removeAttribute("readonly");
    btn.textContent = "Save";
  } else {
    const title = input.value.trim();
    if (title) {
      fetch(`/tasks/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title })
      })
      .then(() => {
        input.setAttribute("readonly", true);
        btn.textContent = "Edit";
        loadTasks();
      });
    }
  }
}

function deleteTask(id) {
  fetch(`/tasks/${id}`, { method: "DELETE" })
    .then(() => loadTasks());
}

function getAISuggestion() {
  fetch("/ai-suggestion")
    .then(res => res.json())
    .then(data => {
      document.getElementById("taskInput").value = data.suggestion;
    })
    .catch(() => {
      document.getElementById("taskInput").value = "Reflect on your goals";
    });
}

// Load tasks when page loads
loadTasks();