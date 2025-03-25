$(document).ready(function () {
    const Toast = Swal.mixin({
        toast: true,
        position: "top",
        showConfirmButton: false,
        timer: 2000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.onmouseenter = Swal.stopTimer;
            toast.onmouseleave = Swal.resumeTimer;
        },
    });
    function generateCartId() {
        // Retrieve the value of "cartId" from local storage and assign it to the variable 'ls_cartId'
        const ls_cartId = localStorage.getItem("cartId");

        // Check if the retrieved value is null (i.e., "cartId" does not exist in local storage)
        if (ls_cartId === null) {
            // Initialize an empty string variable 'cartId' to store the new cart ID
            var cartId = "";

            // Loop 10 times to generate a 10-digit random cart ID
            for (var i = 0; i < 10; i++) {
                // Generate a random number between 0 and 9, convert it to an integer, and append it to 'cartId'
                cartId += Math.floor(Math.random() * 10);
            }

            // Store the newly generated 'cartId' in local storage with the key "cartId"
            localStorage.setItem("cartId", cartId);
        }

        // Return the existing cart ID from local storage if it was found, otherwise return the newly generated 'cartId'
        return ls_cartId || cartId;
    }

    $(document).on("click", ".add_to_cart", function () {
        const button_el = $(this);
        const id = button_el.attr("data-id");
        const qty = $(".quantity").val();
        const size = $("input[name='size']:checked").val();
        const color = $("input[name='color']:checked").val();
        const cart_id = generateCartId();

        $.ajax({
            url: "/add_to_cart/",
            data: {
                id: id,
                qty: qty,
                size: size,
                color: color,
                cart_id: cart_id,
            },
            beforeSend: function () {
                button_el.html('Adding To Cart <i class="fas fa-spinner fa-spin ms-2"></i>');
            },
            success: function (response) {
                console.log(response);
                Toast.fire({
                    icon: "success",
                    title: response.message,
                });
                button_el.html('Added To Cart <i class="fas fa-check-circle ms-2"></i>');
                $(".total_cart_items").text(response.total_cart_items);
            },
            error: function (xhr, status, error) {
                button_el.html('Add To Cart <i class="fas fa-shopping-cart ms-2"></i>');

                console.log("Error Status: " + xhr.status); // Logs the status code, e.g., 400
                console.log("Response Text: " + xhr.responseText); // Logs the actual response text (JSON string)

                // Try parsing the JSON response
                try {
                    let errorResponse = JSON.parse(xhr.responseText);
                    console.log("Error Message: " + errorResponse.error); // Logs "Missing required parameters"
                    Toast.fire({
                        icon: "error",
                        title: errorResponse.error,
                    });
                } catch (e) {
                    console.log("Could not parse JSON response");
                }

                // Optionally show an alert or display the error message in the UI
                console.log("Error: " + xhr.status + " - " + error);
            },
        });
    });

    $(document).on("click", ".update_cart_qty", function () {
        const button_el = $(this);
        const update_type = button_el.attr("data-update_type");
        const product_id = button_el.attr("data-product_id");
        const item_id = button_el.attr("data-item_id");
        const cart_id = generateCartId();
        var qty = $(".item-qty-" + item_id).val();

        if (update_type === "increase") {
            $(".item-qty-" + item_id).val(parseInt(qty) + 1);
            qty++;
        } else {
            if (parseInt(qty) <= 1) {
                $(".item-qty-" + item_id).val(1);
                qty = 1;
            } else {
                $(".item-qty-" + item_id).val(parseInt(qty) - 1);
                qty--;
            }
        }

        $.ajax({
            url: "/add_to_cart/",
            data: {
                id: product_id,
                qty: qty,
                cart_id: cart_id,
            },
            beforeSend: function () {
                button_el.html('<i class="fas fa-spinner fa-spin"></i>');
            },
            success: function (response) {
                Toast.fire({
                    icon: "success",
                    title: response.message,
                });
                if (update_type === "increase") {
                    button_el.html("+");
                } else {
                    button_el.html("-");
                }
                $(".item_sub_total_" + item_id).text(response.item_sub_total);
                $(".cart_sub_total").text(response.cart_sub_total);
            },
            error: function (xhr, status, error) {
                console.log("Error Status: " + xhr.status);
                console.log("Response Text: " + xhr.responseText);
                try {
                    let errorResponse = JSON.parse(xhr.responseText);
                    console.log("Error Message: " + errorResponse.error);
                    alert(errorResponse.error);
                } catch (e) {
                    console.log("Could not parse JSON response");
                }
                console.log("Error: " + xhr.status + " - " + error);
            },
        });
    });

    $(document).on("click", ".delete_cart_item", function () {
        const button_el = $(this);
        const item_id = button_el.attr("data-item_id");
        const product_id = button_el.attr("data-product_id");
        const cart_id = generateCartId();

        $.ajax({
            url: "/delete_cart_item/",
            data: {
                id: product_id,
                item_id: item_id,
                cart_id: cart_id,
            },
            beforeSend: function () {
                button_el.html('<i class="fas fa-spinner fa-spin"></i>');
            },
            success: function (response) {
                Toast.fire({
                    icon: "success",
                    title: response.message,
                });
                $(".total_cart_items").text(response.total_cart_items);
                $(".cart_sub_total").text(response.cart_sub_total);
                $(".item_div_" + item_id).addClass("d-none");
            },
            error: function (xhr, status, error) {
                console.log("Error Status: " + xhr.status);
                console.log("Response Text: " + xhr.responseText);
                try {
                    let errorResponse = JSON.parse(xhr.responseText);
                    console.log("Error Message: " + errorResponse.error);
                    alert(errorResponse.error);
                } catch (e) {
                    console.log("Could not parse JSON response");
                }
                console.log("Error: " + xhr.status + " - " + error);
            },
        });
    });

    const fetchCountry = () => {
        fetch("https://api.ipregistry.co/?key=tryout")
            .then(function (response) {
                return response.json();
            })
            .then(function (payload) {
                console.log(payload.location.country.name + ", " + payload.location.city);
            });
    };
    fetchCountry();

    $(document).on("change", ".search-filter, .category-filter, .rating-filter, input[name='price-filter'], input[name='items-display'], .size-filter, .colors-filter", function () {
        let filters = {
            categories: [],
            rating: [],
            colors: [],
            sizes: [],
            prices: "",
            display: "",
            searchFilter: "",
        };

        $(".category-filter:checked").each(function () {
            filters.categories.push($(this).val());
        });

        $(".rating-filter:checked").each(function () {
            filters.rating.push($(this).val());
        });

        $(".size-filter:checked").each(function () {
            filters.sizes.push($(this).val());
        });

        $(".colors-filter:checked").each(function () {
            filters.colors.push($(this).val());
        });

        filters.display = $("input[name='items-display']:checked").val();
        filters.prices = $("input[name='price-filter']:checked").val();
        filters.searchFilter = $("input[name='search-filter']").val();

        console.log(filters);

        $.ajax({
            url: "/filter_products/",
            method: "GET",
            data: filters,
            success: function (response) {
                // Replace product list with the filtered products
                $("#products-list").html(response.html);
                $(".product_count").html(response.product_count);
            },
            error: function (error) {
                console.log("Error fetching filtered products:", error);
            },
        });
    });

    $(document).on("click", ".reset_shop_filter_btn", function () {
        let filters = {
            categories: [],
            rating: [],
            colors: [],
            sizes: [],
            prices: "",
            display: "",
            searchFilter: "",
        };

        $(".category-filter:checked").each(function () {
            $(this).prop("checked", false);
        });

        $(".rating-filter:checked").each(function () {
            $(this).prop("checked", false);
        });

        $(".size-filter:checked").each(function () {
            $(this).prop("checked", false);
        });

        $(".colors-filter:checked").each(function () {
            $(this).prop("checked", false);
        });

        $("input[name='items-display']").each(function () {
            $(this).prop("checked", false);
        });

        $("input[name='price-filter']").each(function () {
            $(this).prop("checked", false);
        });

        $("input[name='search-filter']").val("");

        Toast.fire({ icon: "success", title: "Filter Reset Successfully" });

        $.ajax({
            url: "/filter_products/",
            method: "GET",
            data: filters,
            success: function (response) {
                // Replace product list with the filtered products
                $("#products-list").html(response.html);
                $(".product_count").html(response.product_count);
            },
            error: function (error) {
                console.log("Error fetching filtered products:", error);
            },
        });
    });

    $(document).on("click", ".add_to_wishlist", function () {
        const button = $(this);
        const product_id = button.attr("data-product_id");
        console.log(product_id);

        $.ajax({
            url: `/customer/add_to_wishlist/${product_id}/`,
            beforeSend: function () {
                button.html("<i class='fas fa-spinner fa-spin text-gray'></i>");
            },
            success: function (response) {
                button.html("<i class='fas fa-heart text-danger'></i>");
                console.log(response);
                if (response.message === "User is not logged in") {
                    button.html("<i class='fas fa-heart text-gray'></i>");

                    Toast.fire({
                        icon: "warning",
                        title: response.message,
                    });
                } else {
                    button.html("<i class='fas fa-heart text-danger'></i>");
                    Toast.fire({
                        icon: "success",
                        title: response.message,
                    });
                }
            },
        });
    });
});
