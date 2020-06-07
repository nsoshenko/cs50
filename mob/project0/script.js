// Variables for classes linkage
const classNames = {
  TODO_ITEM: 'todo-container',
  TODO_CHECKBOX: 'todo-checkbox',
  TODO_TEXT: 'todo-text',
  TODO_DELETE: 'todo-delete',
}

// Targeting elements
const list = document.getElementById('todo-list')
const itemCountSpan = document.getElementById('item-count')
const uncheckedCountSpan = document.getElementById('unchecked-count')

function newTodo() {

  // Get todo text
  const todo = prompt("Enter your TODO here:")

  // Create container
  const li = render('li', 'TODO_ITEM', list)

  // Create checkbox with listener
  const checkbox = render('input', 'TODO_CHECKBOX', li)
  checkbox.type = 'checkbox'
  checkbox.addEventListener('click', () => {
    toggleTodo(checkbox.checked)
  })

  const span = render('span', 'TODO_TEXT', li)
  span.innerHTML = todo

  // Create delete button with listener
  const button = render('button', 'TODO_DELETE', li)
  button.innerHTML = 'DELETE'
  button.addEventListener('click', () => {
    deleteTodo(button, checkbox.checked)
  })

  // Update counters on adding
  itemCountSpan.innerHTML++
  uncheckedCountSpan.innerHTML++
}

// Update counters on toggling a checkbox
function toggleTodo(checked) {
  console.log(checked)
  if (checked) {
    uncheckedCountSpan.innerHTML--
  }
  else {
    uncheckedCountSpan.innerHTML++
  }
}

// Delete todo and update counters
function deleteTodo(button, checked) {
  button.parentElement.remove()
  itemCountSpan.innerHTML--
  if (!checked) {
    uncheckedCountSpan.innerHTML--
  }
}

// Helper function for element creation to keep DRY
function render(elementType, className, parent) {
  const temp = document.createElement(elementType)
  temp.classList.add(classNames[className])
  parent.append(temp)
  return temp
}
