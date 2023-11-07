// Обработка отправки формы входа
$(document).ready(function() {
    $("#loginForm").submit(function(event) {
        event.preventDefault();

        // Проверка логина и пароля (замените на свою логику)
        var email = $("#email").val();
        var password = $("#password").val();

        // Пример: При успешной авторизации перенаправить на cabinet.html
        if (email === "danik12062002@mail.ru" && password === "123") {
            window.location.href = "cabinet.html";
        } else {
            // Обработка ошибки входа (можно добавить уведомление)
            alert("Неверный логин или пароль");
        }

        // Закрытие модального окна
        $("#loginModal").modal("hide");
    });
});

