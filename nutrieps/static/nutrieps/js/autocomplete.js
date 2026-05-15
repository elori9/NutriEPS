$(document).ready(function() {

    $("#searchInput").autocomplete({
        source: function( request, response ) {
            $.ajax({
                url: "/api/foods/",
                dataType: "json",
                data: { q: request.term },
                success: function( data ) {
                    response( $.map( data, function( item ) {
                        return {
                            label: item.name + " (" + item.calories + " Kcal)",
                            value: item.name,
                            calories: item.calories,
                            protein: item.protein,
                            carbs: item.carbs,
                            fat: item.fat
                        }
                    }));
                }
            });
        },
        minLength: 2,
        select: function( event, ui ) {
            if (ui.item) {
                renderSingleCard(ui.item);
            }
        }
    });

    function renderSingleCard(foodItem) {
        const csrfToken = $('[name=csrfmiddlewaretoken]').val();
        const resultsContainer = $("#resultsContainer");
        resultsContainer.empty();

        const cardHtml = `
        <div class="summary-card" style="padding: 1.5rem; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h4 style="font-size: 1.2rem; font-weight: 800; margin-bottom: 0.5rem;">${foodItem.value || foodItem.name}</h4>
                <p style="color: var(--color-text-gray); font-size: 0.9rem; margin-bottom: 1rem;">
                    <strong>${foodItem.calories} Kcal</strong><br>
                    Proteins: ${foodItem.protein}g | Carbs: ${foodItem.carbs}g | Fats: ${foodItem.fat}g
                </p>
            </div>
            <form method="POST" action="${window.ADD_CONSUMPTION_URL}">
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                <input type="hidden" name="food_name" value="${foodItem.value || foodItem.name}">
                <input type="hidden" name="calories" value="${foodItem.calories}">
                <input type="hidden" name="protein" value="${foodItem.protein}">
                <input type="hidden" name="carbs" value="${foodItem.carbs}">
                <input type="hidden" name="fat" value="${foodItem.fat}">

                <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                    <input type="number" name="quantity" value="100" min="1"
                           style="width: 80px; padding: 0.5rem; border: 1px solid #ccc; border-radius: 5px;">
                    <span style="align-self: center; color: var(--color-text-gray);">grams</span>
                </div>
                <button type="submit" class="submit-btn green-btn" style="margin-top: 0;">+ Add to Today</button>
            </form>
        </div>`;

        resultsContainer.append(cardHtml);
    }

    function fetchAllResults() {
        $("#searchInput").autocomplete("close");
        const searchTerm = $("#searchInput").val().trim();
        if (searchTerm.length < 2) return;

        $.ajax({
            url: "/api/foods/",
            dataType: "json",
            data: { q: searchTerm },
            success: function(data) {
                const resultsContainer = $("#resultsContainer");
                resultsContainer.empty();

                if (data.length === 0) {
                    resultsContainer.append('<p style="grid-column: 1/-1; text-align: center; color: gray;">No food found for "' + searchTerm + '".</p>');
                    return;
                }

                $.each(data, function(index, food) {
                    renderSingleCard(food);
                });
            }
        });
    }

    $("#searchBtn").click(function() {
        fetchAllResults();
    });


    $("#searchInput").keypress(function(e) {
        if (e.which == 13) {
            e.preventDefault();
            fetchAllResults();
        }
    });

});
