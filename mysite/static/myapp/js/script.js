function rateProduct(rating, productId) {
    // Удаляем все звезды для конкретного продукта
    const stars = document.getElementById(`productRating${productId}`).children;
    for (let i = 0; i < stars.length; i++) {
        stars[i].classList.remove('fas', 'fa-star');
        stars[i].classList.add('far', 'fa-star');
    }

    // Устанавливаем звезды согласно выбранному рейтингу
    for (let i = 0; i < rating; i++) {
        stars[i].classList.remove('far', 'fa-star');
        stars[i].classList.add('fas', 'fa-star');
    }

    // Здесь вы можете добавить логику сохранения рейтинга для конкретного продукта
    console.log(`Выбран рейтинг ${rating} для продукта ${productId}`);
}
