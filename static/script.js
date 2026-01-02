document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("allocationForm");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(form);

    try {
      const response = await fetch("/allocation", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Request failed");
      }

      const data = await response.json();

      const totalElem = document.getElementById("totalAllocation");

      if (data.total_allocation == 0) {
        totalElem.textContent = "No Allocations Found";
        totalElem.style.color = "red";
        totalElem.style.fontSize = "1.1rem";
      } else {
        totalElem.textContent = typeof data.total_allocation === "number"
          ? data.total_allocation.toFixed(2)
          : data.total_allocation;
        totalElem.style.color = ""; // Reset in case of previous red style
        totalElem.style.fontSize = "2rem"; // Or your desired default
      }

      document.getElementById("xAllocation").textContent =
        typeof data.x_allocation === "number"
          ? data.x_allocation.toFixed(2)
          : data.x_allocation;

      document.getElementById("addressAllocation").textContent =
        typeof data.address_allocation === "number"
          ? data.address_allocation.toFixed(2)
          : data.address_allocation;

      document.getElementById("result").style.display = "flex";
    } catch (error) {
      alert("Error fetching allocation.");
      console.error(error);
    }
  });
});
