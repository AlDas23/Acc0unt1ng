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

  window.onload = function() {
    toggleDateFilter();
  };