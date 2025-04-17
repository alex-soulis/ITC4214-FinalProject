// Alpine.js code for cart functionality
document.addEventListener("DOMContentLoaded", () => {
    function cart() {
        return {
            removeItem(itemId) {
                console.log('Removing item with ID:', itemId);
                // Handle item removal (AJAX request or DOM manipulation)
                // For example:
                const itemElement = document.querySelector(`[data-item-id="${itemId}"]`);
                itemElement.closest('li').remove();  // Remove the item from the list

                // Optionally send an AJAX request to update the cart on the server
                fetch('/remove-item/', {
                    method: 'POST',
                    body: JSON.stringify({ itemId: itemId }),
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value, // Add CSRF token
                    },
                }).then(response => response.json())
                  .then(data => {
                      console.log('Item removed:', data);
                  })
                  .catch(error => {
                      console.error('Error removing item:', error);
                  });
            },

            updateQuantity(itemId, quantity) {
                console.log('Updating item with ID:', itemId, 'to quantity', quantity);
                // Handle quantity update (AJAX request or DOM manipulation)
                // For example, update the cart UI or send AJAX request to update on the server.
            }
        }
    }

    // Initialize Alpine.js on the page
    window.cart = cart;
});
