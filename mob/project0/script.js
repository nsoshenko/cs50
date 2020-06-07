const classNames = {
  TODO_ITEM: 'todo-container',
  TODO_CHECKBOX: 'todo-checkbox',
  TODO_TEXT: 'todo-text',
  TODO_DELETE: 'todo-delete',
}

const list = document.getElementById('todo-list')
const itemCountSpan = document.getElementById('item-count')
const uncheckedCountSpan = document.getElementById('unchecked-count')
//let counter = 1

function newTodo() {
  const todo = prompt("Enter your TODO here:")

  const li = render('li', 'TODO_ITEM', list)
  //li.setAttribute('dataset-id', counter++)

  const checkbox = render('input', 'TODO_CHECKBOX', li)
  checkbox.type = 'checkbox'
  checkbox.addEventListener('click', () => {
    toggleTodo(checkbox.checked)
  })

  const span = render('span', 'TODO_TEXT', li)
  span.innerHTML = todo

  const button = render('button', 'TODO_DELETE', li)
  button.innerHTML = 'DELETE'
  button.addEventListener('click', () => {
    deleteTodo(button, checkbox.checked)
  })
  //button.setAttribute('onclick', 'deleteTodo(parentElement.data.id)')

  itemCountSpan.innerHTML++
  uncheckedCountSpan.innerHTML++
}

function toggleTodo(checked) {
  console.log(checked)
  if (checked) {
    uncheckedCountSpan.innerHTML--
  }
  else {
    uncheckedCountSpan.innerHTML++
  }
}

function deleteTodo(button, checked) {
  button.parentElement.remove()
  itemCountSpan.innerHTML--
  if (!checked) {
    uncheckedCountSpan.innerHTML--
  }
}

function render(elementType, className, parent) {
  const temp = document.createElement(elementType)
  temp.classList.add(classNames[className])
  parent.append(temp)
  return temp
}
