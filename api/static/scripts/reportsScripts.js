function toggleDateFilter() {
    const checkbox = document.getElementById('date-checkbox');
    const startDate = document.getElementById('start-date');
    const startLabel = document.getElementById('start-date-label');
    const endLabel = document.getElementById('end-date-label');
    const endDate = document.getElementById('end-date');
    if (checkbox.checked) {
      startDate.disabled = false;
      startDate.style.visibility = "visible";
      startLabel.style.visibility = "visible";
      endDate.disabled = false;
      endDate.style.visibility = "visible";
      endLabel.style.visibility = "visible";
    } else {
      startDate.disabled = true;
      startDate.style.visibility = "hidden";
      startLabel.style.visibility = "hidden";
      endDate.disabled = true;
      endDate.style.visibility = "hidden";
      endLabel.style.visibility = "hidden";
    }
  }

function toggleCurrFilter() {
    const checkbox = document.getElementById('curr-checkbox');
    const eurLabel = document.getElementById('eur-label');
    const eurCheckbox = document.getElementById('currency-eur');
    const usdLabel = document.getElementById('usd-label');
    const usdCheckbox = document.getElementById('currency-usd');
    const ronLabel = document.getElementById('ron-label');
    const ronCheckbox = document.getElementById('currency-ron');
    const uahLabel = document.getElementById('uah-label');
    const uahCheckbox = document.getElementById('currency-uah');
;
    if (checkbox.checked) {
      eurLabel.disabled = true;
      eurLabel.style.visibility = "hidden";
      eurCheckbox.disabled = true;
      eurCheckbox.style.visibility = "hidden";
      usdLabel.disabled = true;
      usdLabel.style.visibility = "hidden";
      usdCheckbox.disabled = true;
      usdCheckbox.style.visibility = "hidden";
      ronLabel.disabled = true;
      ronLabel.style.visibility = "hidden";
      ronCheckbox.disabled = true;
      ronCheckbox.style.visibility = "hidden";
      uahLabel.disabled = true;
      uahLabel.style.visibility = "hidden";
      uahCheckbox.disabled = true;
      uahCheckbox.style.visibility = "hidden";

    } else {
      eurLabel.disabled = false;
      eurLabel.style.visibility = "visible";
      eurCheckbox.disabled = false;
      eurCheckbox.style.visibility = "visible";
      usdLabel.disabled = false;
      usdLabel.style.visibility = "visible";
      usdCheckbox.disabled = false;
      usdCheckbox.style.visibility = "visible";
      ronLabel.disabled = false;
      ronLabel.style.visibility = "visible";
      ronCheckbox.disabled = false;
      ronCheckbox.style.visibility = "visible";
      uahLabel.disabled = false;
      uahLabel.style.visibility = "visible";
      uahCheckbox.disabled = false;
      uahCheckbox.style.visibility = "visible";
    }
}

function generateReport() {
  // JavaScript code to handle form submission and generate report
  const form = document.getElementById('report-form');
  const formData = new FormData(form);
  // Process formData and generate report table
  // This part will involve making a request to the server and updating the table
}

  window.onload = function() {
    toggleDateFilter();
    toggleCurrFilter();
  };