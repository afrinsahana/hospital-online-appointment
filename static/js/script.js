async function askAI() {

    const input =
        document.getElementById("message");

    const chat =
        document.getElementById("chatBox");

    const message =
        input.value.trim();

    if (!message) {
        return;
    }

    chat.innerHTML += `
        <div class="user-message">
            <strong>You:</strong>
            ${message}
        </div>
    `;

    input.value = "";

    try {

        const response =
            await fetch("/api/ai-assistant", {

                method: "POST",

                headers: {
                    "Content-Type":
                    "application/json"
                },

                body: JSON.stringify({
                    message: message
                })
            });


        const data =
            await response.json();


        chat.innerHTML += `
            <div class="ai-message">
                <strong>AI:</strong>
                ${data.reply}
            </div>
        `;


        if (data.doctors.length > 0) {

            data.doctors.forEach(
                doctor => {

                    chat.innerHTML += `
                        <div class="doctor-result">

                            <strong>
                                ${doctor.name}
                            </strong>

                            <br>

                            ${doctor.specialization}

                            <br>

                            ${doctor.hospital_name}

                            <br>

                            <a
                            href="/appointment/${doctor.id}"
                            class="btn btn-sm btn-success mt-2">

                            Book Appointment

                            </a>

                        </div>
                    `;
                }
            );
        }

    } catch (error) {

        chat.innerHTML += `
            <div class="alert alert-danger">
                AI assistant is temporarily unavailable.
            </div>
        `;
    }
}
