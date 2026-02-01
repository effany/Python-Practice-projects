// add button logic

const addButtons = document.querySelectorAll('.add-to-cart-btn')

addButtons.forEach(button => {
    button.addEventListener('click', async function() {
        // Get item data from this button
        const itemName = this.dataset.itemName
        const itemId = this.dataset.itemId
        const itemSku = this.dataset.itemSku
        const itemPrice = this.dataset.itemPrice
        const itemDiscountPrice = this.dataset.itemDiscountPrice
        const itemImageUrl = this.dataset.itemImageUrl
        
        try {
            const response = await fetch('/add-to-cart', {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'itemName': itemName, 
                    'itemId': itemId, 
                    'itemSku': itemSku,
                    'itemPrice': itemPrice,
                    'itemDiscountPrice': itemDiscountPrice,
                    'itemImageUrl': itemImageUrl,
                    'itemCount': 1
                })
            })
            
            // Parse JSON response
            const data = await response.json()
            
            // Handle success
            if (data.success) {
                alert('Item added to cart!')
                location.reload()
                // Update cart count if you have a badge element
                // const cartBadge = document.querySelector('#cart-count')
                // if (cartBadge) cartBadge.textContent = data.cart_count
            } else {
                alert('Failed to add item: ' + data.message)
            }
            
        } catch (error) {
            console.error('Error:', error)
            alert('An error occurred while adding to cart')
        }
    })
})

// remove button logic

const removeButtons = document.querySelectorAll('.remove-from-cart-btn')

removeButtons.forEach(button => {
    button.addEventListener('click', async function() {
        const itemName = this.dataset.itemName
        const itemId = this.dataset.itemId
        const itemSku = this.dataset.itemSku
        const itemPrice = this.dataset.itemPrice
        const itemDiscountPrice = this.dataset.itemDiscountPrice
        const itemImageUrl = this.dataset.itemImageUrl

        try {
            const response = await fetch('/remove-from-cart', {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'itemName': itemName, 
                    'itemId': itemId, 
                    'itemSku': itemSku,
                    'itemPrice': itemPrice,
                    'itemDiscountPrice': itemDiscountPrice,
                    'itemImageUrl': itemImageUrl,
                    'itemCount': 1
                })
            })
            
            // Parse JSON response
            const data = await response.json()
            
            // Handle success
            if (data.success) {
                alert('Item removed from cart!')
                location.reload()
                // Update cart count if you have a badge element
                // const cartBadge = document.querySelector('#cart-count')
                // if (cartBadge) cartBadge.textContent = data.cart_count
            } else {
                alert('Failed to remove item: ' + data.message)
            }
            
        } catch (error) {
            console.error('Error:', error)
            alert('An error occurred while adding to cart')
        }
    })
})