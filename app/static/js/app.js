function getToken() {
    return localStorage.getItem("token") || "";
}


async function api(
    path,
    options = {}
) {

    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };


    const token =
        getToken();


    if (token) {

        headers.Authorization =
            "Bearer " + token;

    }


    const response =
        await fetch(
            path,
            {
                ...options,
                headers
            }
        );


    let data = {};

    try {

        data =
            await response.json();

    } catch {

        data = {};

    }


    if (
        response.status === 401
        && path !== "/token"
    ) {

        localStorage.removeItem(
            "token"
        );

    }


    return data;
}


const logoutButton =
    document.querySelector(
        "#logoutBtn"
    );


if (logoutButton) {

    logoutButton.addEventListener(
        "click",
        async function() {

            if (getToken()) {

                await api(
                    "/logout",
                    {
                        method: "POST"
                    }
                );

            }

            localStorage.removeItem(
                "token"
            );

            location.href =
                "/login";

        }
    );

}


function escapeHtml(value) {

    return String(
        value ?? ""
    ).replace(
        /[&<>"']/g,
        function(character) {

            const map = {

                "&": "&amp;",
                "<": "&lt;",
                ">": "&gt;",
                '"': "&quot;",
                "'": "&#039;"

            };

            return map[
                character
            ];

        }
    );
}


function renderResults(data) {

    const results =
        document.getElementById(
            "results"
        );


    results.innerHTML = `

        <div class="card">

            <div class="result-head">

                <div>

                    <p class="eyebrow">

                        ${escapeHtml(
                            data.planner
                                .toUpperCase()
                        )}

                        ·

                        ${escapeHtml(
                            data.source
                        )}

                    </p>


                    <h2>

                        ${escapeHtml(
                            data.summary
                        )}

                    </h2>

                </div>


                <div>

                    <b>
                        Budget
                    </b>

                    <br>

                    ₹${Number(
                        data.budget
                    ).toLocaleString()}


                    <br><br>


                    <b>
                        Estimated
                    </b>

                    <br>

                    ₹${Number(
                        data.estimated_total
                    ).toLocaleString()}

                </div>

            </div>


            <p>

                <b>
                    Remaining:
                </b>

                ₹${Number(
                    data.remaining
                ).toLocaleString()}

            </p>


            <div class="recommendations">

                ${
                    data.recommendations
                        .map(
                            item => `

                            <article
                                class="rec"
                            >

                                <span
                                    class="tag"
                                >

                                    ${escapeHtml(
                                        item.platform
                                    )}

                                </span>


                                <h3>

                                    ${escapeHtml(
                                        item.name
                                    )}

                                </h3>


                                <p>

                                    ${escapeHtml(
                                        item.reason
                                    )}

                                </p>


                                <div
                                    class="price"
                                >

                                    ₹${Number(
                                        item.price
                                    ).toLocaleString()}

                                    ×

                                    ${item.quantity}

                                    =

                                    ₹${Number(
                                        item.total
                                    ).toLocaleString()}

                                </div>


                                <a
                                    target="_blank"
                                    rel="noopener"
                                    href="${item.url}"
                                >
                                    Open destination →
                                </a>

                            </article>

                            `
                        )
                        .join("")
                }

            </div>


            <h3>
                Notes
            </h3>


            <ul>

                ${
                    (
                        data.ai_notes || []
                    )
                    .map(
                        note => `

                        <li>
                            ${escapeHtml(
                                note
                            )}
                        </li>

                        `
                    )
                    .join("")
                }

            </ul>

        </div>
    `;
}


function plannerJsonForm(
    endpoint,
    getData
) {

    const form =
        document.getElementById(
            "plannerForm"
        );


    form.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const message =
                document.getElementById(
                    "msg"
                );


            message.textContent =
                "Generating...";


            const data =
                await api(
                    endpoint,
                    {
                        method: "POST",

                        body:
                            JSON.stringify(
                                getData()
                            )
                    }
                );


            if (
                data.recommendations
            ) {

                message.textContent =
                    "";

                renderResults(
                    data
                );

            } else {

                message.textContent =
                    data.detail ||
                    "Please login first.";

            }

        }
    );
}


function plannerFormJewelry() {

    const form =
        document.getElementById(
            "plannerForm"
        );


    form.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const message =
                document.getElementById(
                    "msg"
                );


            message.textContent =
                "Generating...";


            const formData =
                new FormData();


            formData.append(
                "budget",
                document.getElementById(
                    "budget"
                ).value
            );


            formData.append(
                "occasion",
                document.getElementById(
                    "occasion"
                ).value
            );


            formData.append(
                "style",
                document.getElementById(
                    "style"
                ).value
            );


            formData.append(
                "preferences",
                document.getElementById(
                    "preferences"
                ).value
            );


            const imageInput =
                document.getElementById(
                    "outfit_image"
                );


            if (
                imageInput.files.length
            ) {

                formData.append(
                    "outfit_image",
                    imageInput.files[0]
                );

            }


            const response =
                await fetch(
                    "/generate-jewelry",
                    {
                        method: "POST",

                        headers: {
                            Authorization:
                                "Bearer " +
                                getToken()
                        },

                        body: formData
                    }
                );


            let data = {};

            try {

                data =
                    await response.json();

            } catch {

                data = {};

            }


            if (
                data.recommendations
            ) {

                message.textContent =
                    "";

                renderResults(
                    data
                );

            } else {

                message.textContent =
                    data.detail ||
                    "Please login first.";

            }

        }
    );
}