const puzzle = [
      [5,3,0,0,7,0,0,0,0],
      [6,0,0,1,9,5,0,0,0],
      [0,9,8,0,0,0,0,6,0],
      [8,0,0,0,6,0,0,0,3],
      [4,0,0,8,0,3,0,0,1],
      [7,0,0,0,2,0,0,0,6],
      [0,6,0,0,0,0,2,8,0],
      [0,0,0,4,1,9,0,0,5],
      [0,0,0,0,8,0,0,7,9]
    ];

    let selected = null;
    const board = document.getElementById("board");
    const numbers = document.getElementById("numbers");
    const message = document.getElementById("message");

    function drawBoard() {
      board.innerHTML = "";
      numbers.innerHTML = "";

      for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
          const cell = document.createElement("input");
          cell.className = "cell";
          cell.type = "text";
          cell.inputMode = "none";
          cell.maxLength = 1;
          cell.dataset.row = r;
          cell.dataset.col = c;
          cell.setAttribute("aria-label", `Row ${r+1}, column ${c+1}`);

          if (puzzle[r][c] !== 0) {
            cell.value = puzzle[r][c];
            cell.classList.add("given");
            cell.readOnly = true;
          }

          cell.addEventListener("focus", () => {
            selected = { r, c };
            updateSelection();
          });

          cell.addEventListener("input", () => {
            const digit = cell.value.replace(/[^1-9]/g, "");
            cell.value = digit.slice(-1);
            message.textContent = "";
          });

          cell.addEventListener("keydown", e => {
            if (e.key === "Backspace" || e.key === "Delete") {
              if (!cell.readOnly) cell.value = "";
            }
          });

          board.appendChild(cell);
        }
      }

      for (let n = 1; n <= 9; n++) {
        const button = document.createElement("button");
        button.textContent = n;
        button.onclick = () => enterNumber(n);
        numbers.appendChild(button);
      }
    }

    function updateSelection() {
      document.querySelectorAll(".cell").forEach(cell => {
        cell.classList.remove("selected");
        if (
          selected &&
          Number(cell.dataset.row) === selected.r &&
          Number(cell.dataset.col) === selected.c
        ) {
          cell.classList.add("selected");
        }
      });
    }

    function enterNumber(n) {
      if (!selected) {
        message.textContent = "Select an empty cell first.";
        return;
      }

      const cell = document.querySelector(
        `.cell[data-row="${selected.r}"][data-col="${selected.c}"]`
      );

      if (!cell.readOnly) {
        cell.value = n;
        message.textContent = "";
        cell.focus();
      }
    }

    function eraseCell() {
      if (!selected) return;

      const cell = document.querySelector(
        `.cell[data-row="${selected.r}"][data-col="${selected.c}"]`
      );

      if (!cell.readOnly) cell.value = "";
      message.textContent = "";
    }

    function checkBoard() {
      const cells = [...document.querySelectorAll(".cell")];
      let complete = true;
      let errors = 0;

      cells.forEach(cell => {
        cell.classList.remove("error");
      });

      function get(r, c) {
        return cells[r * 9 + c].value;
      }

      function conflict(r, c) {
        const value = get(r, c);
        if (!value) return false;

        for (let i = 0; i < 9; i++) {
          if (i !== c && get(r, i) === value) return true;
          if (i !== r && get(i, c) === value) return true;
        }

        const br = Math.floor(r / 3) * 3;
        const bc = Math.floor(c / 3) * 3;

        for (let y = br; y < br + 3; y++) {
          for (let x = bc; x < bc + 3; x++) {
            if ((y !== r || x !== c) && get(y, x) === value) {
              return true;
            }
          }
        }

        return false;
      }

      cells.forEach(cell => {
        const r = Number(cell.dataset.row);
        const c = Number(cell.dataset.col);

        if (!cell.value) complete = false;

        if (conflict(r, c)) {
          cell.classList.add("error");
          errors++;
        }
      });

      if (errors) {
        message.textContent = "Conflicts found. Check the red cells.";
        message.style.color = "#dc2626";
      } else if (!complete) {
        message.textContent = "No conflicts so far. Keep solving!";
        message.style.color = "#2563eb";
      } else {
        message.textContent = "All rows, columns and boxes are valid!";
        message.style.color = "#16a34a";
      }
    }

    function resetBoard() {
      drawBoard();
      selected = null;
      message.textContent = "";
    }

    drawBoard();