async function getSession() {

    const response =
        await fetch(
            "/api/auth/session-info"
        );

    if (response.ok) {

        return await response.json();

    }

    return null;
}


async function updateAuthLink() {

    const link =
        document.getElementById(
            "authLink"
        );

    if (!link) {

        return;
    }


    const session =
        await getSession();


    if (session) {

        link.textContent =
            "Dashboard";

        link.href =
            "/dashboard";

    }

}


function setupPlanner(
    formId,
    endpoint,
    makePayload
) {

    const form =
        document.getElementById(
            formId
        );

    if (!form) {

        return;
    }


    form.addEventListener(
        "submit",
        async event => {

            event.preventDefault();


            const result =
                document.getElementById(
                    "result"
                );


            const error =
                document.getElementById(
                    "error"
                );


            error.textContent =
                "";


            result.innerHTML =
                `
                <div class="loading">
                    Thinking...
                </div>
                `;


            const body =
                makePayload(
                    new FormData(form)
                );


            const response =
                await fetch(
                    endpoint,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                body
                            )
                    }
                );


            const data =
                await response.json();


            if (
                response.status === 401
            ) {

                location.href =
                    "/login";

                return;
            }


            if (!response.ok) {

                result.innerHTML =
                    "";

                error.textContent =
                    data.detail
                    ||
                    "Could not generate recommendations.";

                return;
            }


            renderRecommendation(
                result,
                data
            );

        }
    );

}


function renderRecommendation(
    container,
    data
) {

    const allocation =
        Object.entries(
            data.allocation || {}
        )
        .map(
            ([key, value]) =>

                `
                <div>

                    <b>
                        ${escapeHtml(key)}
                    </b>

                    <small>
                        ₹${Number(value)
                            .toLocaleString("en-IN")}
                    </small>

                </div>
                `
        )
        .join("");


    const recommendations =
        (
            data.recommendations
            ||
            []
        )
        .map(
            item =>

                `
                <article
                    class="recommendation"
                >

                    <div
                        class="recommendation-top"
                    >

                        <div>

                            <span class="tag">

                                ${escapeHtml(
                                    item.category
                                    ||
                                    "option"
                                )}

                            </span>

                            <h3>

                                ${escapeHtml(
                                    item.title
                                    ||
                                    "Recommendation"
                                )}

                            </h3>

                        </div>


                        <div class="price">

                            ₹${Number(
                                item.price
                                ||
                                0
                            ).toLocaleString(
                                "en-IN"
                            )}

                        </div>

                    </div>


                    <p>

                        ${escapeHtml(
                            item.description
                            ||
                            ""
                        )}

                    </p>


                    <p class="muted">

                        ${escapeHtml(
                            item.reason
                            ||
                            ""
                        )}

                    </p>


                    <small>

                        ${escapeHtml(
                            item.platform
                            ||
                            ""
                        )}

                    </small>


                    ${
                        item.url
                        ?
                        `
                        <br>

                        <a
                            href="${safeUrl(
                                item.url
                            )}"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            Open platform
                        </a>
                        `
                        :
                        ""
                    }

                </article>
                `
        )
        .join("");


    const tips =
        (
            data.tips
            ||
            []
        )
        .map(
            tip =>
                `
                <li>
                    ${escapeHtml(tip)}
                </li>
                `
        )
        .join("");


    container.innerHTML =

        `

        <div class="result-card">

            <span class="tag">

                ${escapeHtml(
                    data.ai_mode
                    ||
                    "fallback"
                )}
                mode

            </span>


            <h2>

                ${escapeHtml(
                    data.summary
                    ||
                    "Your plan"
                )}

            </h2>


            <p class="muted">

                Budget:
                ₹${Number(
                    data.budget
                    ||
                    0
                ).toLocaleString(
                    "en-IN"
                )}

            </p>


            ${
                allocation
                ?
                `
                <div class="allocation">
                    ${allocation}
                </div>
                `
                :
                ""
            }


            ${
                data.outfit_analysis
                ?
                `
                <p>

                    <b>
                        Outfit insight:
                    </b>

                    ${escapeHtml(
                        data.outfit_analysis
                    )}

                </p>
                `
                :
                ""
            }

        </div>


        ${recommendations}


        ${
            tips
            ?
            `
            <div class="result-card">

                <h3>
                    Smart tips
                </h3>

                <ul class="tips">
                    ${tips}
                </ul>

            </div>
            `
            :
            ""
        }

        `;
}


function escapeHtml(value) {

    return String(value).replace(
        /[&<>"']/g,
        character => ({

            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#039;"

        }[character])
    );
}


function safeUrl(url) {

    try {

        const parsed =
            new URL(url);


        if (
            parsed.protocol === "https:"
            ||
            parsed.protocol === "http:"
        ) {

            return parsed.href;

        }

    } catch (error) {

        return "#";

    }

    return "#";
}


updateAuthLink();