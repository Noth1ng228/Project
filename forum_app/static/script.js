document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("addBtn");
    const input = document.getElementById("content");
    const message = document.getElementById("message");
    const postsDiv = document.getElementById("posts");

    function showMessage(text) {
        message.textContent = text;
        setTimeout(() => message.textContent = "", 2000);
    }

    //add 
    btn.addEventListener("click", async () => {
        const text = input.value.trim();
        if (!text) return showMessage("The entry can't be empty.");

        const response = await fetch("/add_ajax", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content: text })
        });

        const result = await response.json();
        if (result.status === "success") {
            const newPost = document.createElement("div");
            newPost.className = "post";
            newPost.dataset.id = result.id;
            newPost.innerHTML = `
                <p class="text">${result.content}</p>
                <div class="actions">
                    <button class="edit">edit</button>
                    <button class="delete">🗑️</button>
                </div>`;
            postsDiv.prepend(newPost);
            input.value = "";
            showMessage("Entry added");
        } else {
            showMessage(result.message);
        }
    });

    //delete
    postsDiv.addEventListener("click", async (e) => {
        const postDiv = e.target.closest(".post");
        const id = postDiv?.dataset.id;

        if (e.target.classList.contains("delete")) {
            const res = await fetch(`/delete_ajax/${id}`, { method: "DELETE" });
            const result = await res.json();
            if (result.status === "success") {
                postDiv.remove();
                showMessage("Entry has deleted");
            } else showMessage(result.message);
        }

        //edit
        if (e.target.classList.contains("edit")) {
            const textEl = postDiv.querySelector(".text");
            const oldText = textEl.textContent;
            const newText = prompt("Edit entry:", oldText);
            if (newText === null) return;

            const res = await fetch(`/edit_ajax/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ content: newText })
            });

            const result = await res.json();
            if (result.status === "success") {
                textEl.textContent = result.content;
                showMessage("Entry has edited");
            } else showMessage(result.message);
        }
    });
    //REPLIES 
postsDiv.addEventListener("click", async (e) => {
    const postDiv = e.target.closest(".post");
    const replyDiv = e.target.closest(".reply");

    // Add reply
    if (e.target.classList.contains("reply-btn")) {
        const postId = postDiv.dataset.id;
        const input = postDiv.querySelector(".reply-input");
        const text = input.value.trim();
        if (!text) return showMessage("The reply can't be empty.");

        const res = await fetch(`/add_reply/${postId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content: text })
        });

        const result = await res.json();
        if (result.status === "success") {
            const repliesDiv = postDiv.querySelector(".replies");
            const newReply = document.createElement("div");
            newReply.className = "reply";
            newReply.dataset.id = result.id;
            newReply.innerHTML = `
                <p class="reply-text">${result.content}</p>
                <div class="reply-actions">
                    <button class="edit-reply">Edit</button>
                    <button class="delete-reply">🗑️</button>
                </div>`;
            repliesDiv.appendChild(newReply);
            input.value = "";
            showMessage("Reply added.");
        } else {
            showMessage(result.message);
        }
    }

    // Edit reply
    if (e.target.classList.contains("edit-reply")) {
        const replyId = replyDiv.dataset.id;
        const textEl = replyDiv.querySelector(".reply-text");
        const oldText = textEl.textContent;
        const newText = prompt("Edit reply:", oldText);
        if (newText === null) return;

        const res = await fetch(`/edit_reply/${replyId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content: newText })
        });

        const result = await res.json();
        if (result.status === "success") {
            textEl.textContent = result.content;
            showMessage("Reply edited.");
        } else showMessage(result.message);
    }

    // Delete reply
    if (e.target.classList.contains("delete-reply")) {
        const replyId = replyDiv.dataset.id;
        const res = await fetch(`/delete_reply/${replyId}`, { method: "DELETE" });
        const result = await res.json();
        if (result.status === "success") {
            replyDiv.remove();
            showMessage("Reply deleted.");
        } else showMessage(result.message);
    }
});
});

