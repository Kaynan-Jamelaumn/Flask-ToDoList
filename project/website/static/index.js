function deleteTask(taskId) {
    fetch("/delete-task", {
        method: "POST",
        body: JSON.stringify({ taskId: taskId }),
    }).then((_res) => {
        const taskElement = document.getElementById(`task-${taskId}`);
        if (taskElement) {
            taskElement.remove();
        }
    }).catch((err) => console.log(err));
}

function reviveTask(taskId) {
    fetch("/revive-task", {
        method: "POST",
        body: JSON.stringify({ taskId: taskId }),
    }).then((_res) => {
        const taskElement = document.getElementById(`task-${taskId}`);
        if (taskElement) {
            taskElement.remove();
        }
    }).catch((err) => console.log(err));
}

// function updateTaskPage(taskID){
//     fetch("/update-task-request", {
//         method: "POST",
//         body: JSON.stringify({ taskId: taskID }),
//     }).then((_res) => {
//         console.log("a")
//         //window.location.href = "/";
//     }).catch((err) => console.log(err));
// }