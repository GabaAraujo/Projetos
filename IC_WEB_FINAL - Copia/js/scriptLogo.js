const container = document.querySelector(".container");
const linkItems = document.querySelectorAll(".link-item");
const dashboardsMenu = document.querySelector('.link-item[data-menu="dashboards"]');
const submenu = dashboardsMenu.querySelector('.submenu');
const submenuIcon = dashboardsMenu.querySelector('.submenu-icon');

// Container Hover
container.addEventListener("mouseenter", () => {
  container.classList.add("active");
});

// Container Hover Leave
container.addEventListener("mouseleave", () => {
  container.classList.remove("active");
});

// Link-items Clicked
linkItems.forEach(linkItem => {
  linkItem.addEventListener("click", (e) => {
    // Check if the clicked item has a submenu
    const submenu = linkItem.querySelector(".submenu");
    const submenuIcon = linkItem.querySelector(".submenu-icon");

    if (submenu) {
      e.preventDefault(); // Prevent default link behavior if there is a submenu
      const isActive = linkItem.classList.contains("active");

      // Toggle active class
      linkItem.classList.toggle("active", !isActive);

      // Show or hide submenu
      submenu.classList.toggle("visible", !isActive);
      submenuIcon.setAttribute("name", isActive ? "chevron-down-outline" : "chevron-up-outline");

      // Close other submenus
      linkItems.forEach(otherItem => {
        if (otherItem !== linkItem) {
          otherItem.classList.remove("active");
          const otherSubmenu = otherItem.querySelector(".submenu");
          const otherSubmenuIcon = otherItem.querySelector(".submenu-icon");
          if (otherSubmenu) {
            otherSubmenu.classList.remove("visible");
          }
          if (otherSubmenuIcon) {
            otherSubmenuIcon.setAttribute("name", "chevron-down-outline");
          }
        }
      });
    } else {
      // Remove active class from all items and add to the clicked one
      linkItems.forEach(item => item.classList.remove("active"));
      linkItem.classList.add("active");
    }
  });
});

// Handle submenu item clicks
document.querySelectorAll('.submenu li a').forEach(submenuItem => {
  submenuItem.addEventListener('click', function (e) {
    e.stopPropagation(); // Prevent the click event from bubbling up
    // Remove 'active' class from all submenu items
    document.querySelectorAll('.submenu li a').forEach(item => item.classList.remove('active'));
    // Add 'active' class to the clicked item
    this.classList.add('active');
  });
});
