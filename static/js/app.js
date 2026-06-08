
let cart = JSON.parse(localStorage.getItem("cart")) || [];

function addToCart(name, price, image){

    cart.push({
    name,
    price,
    image
    });

    localStorage.setItem(
        "cart",
        JSON.stringify(cart)
    );

    alert("Producto agregado");

    updateCartCounter();
}

function removeFromCart(index){

    cart.splice(index, 1);

    localStorage.setItem(
        "cart",
        JSON.stringify(cart)
    );

    location.reload();
}

function clearCart(){

    localStorage.removeItem("cart");

    cart = [];

    updateCartCounter();

    location.reload();
}

function loadCart(){

    const cartItems =
        document.getElementById("cart-items");

    if(!cartItems) return;

    let total = 0;

    cart.forEach((product, index) => {

        total += product.price;

        cartItems.innerHTML += `

    <div class="card">

        <img
            src="/static/images/${product.image}"
            class="cart-image"
        >

        <h2>${product.name}</h2>

        <p>₡ ${product.price}</p>

        <button onclick="removeFromCart(${index})">
            Eliminar
        </button>

    </div>

`;
    });

    document.getElementById("total").innerText =
        "Total: ₡ " + total;
}

async function submitOrder(){

    if(cart.length === 0){

        alert("Carrito vacío");

        return;
    }

    let total = 0;

    cart.forEach(product => {

        total += product.price;
    });

    const response = await fetch('/submit-order', {

        method: 'POST',

        headers: {
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({

            products: cart,
            total: total
        })
    });

    if(response.redirected){

        window.location.href = response.url;

        return;
    }

    const data = await response.json();

    alert(data.message);

    localStorage.removeItem("cart");

    location.reload();
}

function updateCartCounter(){

    const counter =
        document.getElementById(
            "cart-counter"
        );

    if(!counter) return;

    counter.innerText =
        `Carrito 🛒 (${cart.length})`;
}

loadCart();

updateCartCounter();