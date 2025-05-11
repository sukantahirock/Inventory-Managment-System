const menuToggle = document.getElementById("menu-toggle");
const wrapper = document.getElementById("wrapper");
const sidebar = document.getElementById("sidebar-wrapper");

menuToggle.addEventListener("click", function() {
    wrapper.classList.toggle("toggled");
    
    // Force redraw (fixes rendering glitches)
    setTimeout(() => {
        window.dispatchEvent(new Event('resize'));
    }, 10);
});