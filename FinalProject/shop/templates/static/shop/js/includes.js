document.addEventListener("DOMContentLoaded", async () => {
    const includes = document.querySelectorAll("[data-include]");
    const fetches = [];

    includes.forEach((el) => {
        const url = el.getAttribute("data-include");
        fetches.push(
            fetch(url)
                .then((res) => {
                    if (!res.ok) throw new Error(`Failed to fetch ${url}`);
                    return res.text();
                })
                .then((html) => {
                    const wrapper = document.createElement("div");
                    wrapper.innerHTML = html;

                    // If the included file has a single root element like <nav>, preserve it directly
                    const children = wrapper.children;
                    if (children.length === 1) {
                        el.replaceWith(children[0]);
                    } else {
                        el.innerHTML = html;
                    }
                })
                .catch((err) => {
                    console.error("Include error:", err);
                })
        );
    });

    function removeItem(itemId) {
        console.log('Removing item with ID:', itemId);
        // Add the necessary logic to remove the item from the cart.
    }

    // Wait for all includes to be completed
    await Promise.all(fetches);
});
