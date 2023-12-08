$(document).ready(function() {
    $('.rating-form input').change(function() {
        $(this).closest('form').submit();
    });

    $('.rating-form').submit(function(event) {
        event.preventDefault();
        const form = $(this);
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function(response) {
                // Обновляем звезды на странице
                const productId = response.product_id;
                const ratingStars = response.rating_stars;
                const emptyStars = response.empty_stars;
                const ratingSpan = $('#productRating' + productId);
                ratingSpan.empty();
                for (let i = 0; i < ratingStars; i++) {
                    ratingSpan.append('<i class="fas fa-star"></i>');
                }
                for (let i = 0; i < emptyStars; i++) {
                    ratingSpan.append('<i class="far fa-star"></i>');
                }
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    });
});



    // Обработчик отправки формы поиска
    $(document).ready(function () {
        $('form#search-form').submit(function (event) {
            event.preventDefault();
            var form = $(this);
            var url = form.attr('action');
            var formData = form.serialize();

            // Загружаем результаты поиска в модальное окно
            $.ajax({
                type: 'GET',
                url: url,
                data: formData,
                success: function (data) {
                    $('#search-results').html(data);
                    $('#searchModal').modal('show');
                }
            });
        });
    });