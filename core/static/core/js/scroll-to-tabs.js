document.addEventListener("DOMContentLoaded", function () {
    // Define media query for large screens
    var largeScreenQuery = window.matchMedia("(min-width: 992px)"); // Bootstrap lg breakpoint is 992px

    function handleTabClick(event) {
      // Check if the screen size matches the large screens media query
      if (largeScreenQuery.matches) {
        return; // Do nothing for large screens
      }

      // Prevent default behavior
      event.preventDefault();

      // Handle tab activation
      var target = document.querySelector(
        this.getAttribute("data-bs-target")
      );
      var tabInstance = new bootstrap.Tab(this);
      tabInstance.show();

      // Smooth scroll to the tab content
      target.scrollIntoView({ behavior: "smooth" });

      // Smooth scroll to the service-description section
      var serviceDescription = document.getElementById("service-description");
      if (serviceDescription) {
        serviceDescription.scrollIntoView({ behavior: "smooth" });
      }
    }

    // Attach event listeners to tab links
    var tabLinks = document.querySelectorAll(".navlink");
    tabLinks.forEach(function (tabLink) {
      tabLink.addEventListener("click", handleTabClick);
    });
  });