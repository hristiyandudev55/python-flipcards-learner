describe('FlipCards Tests', () => {
  beforeEach(() => {
    cy.visit('http://localhost:5173/category')
    cy.wait(1000)
  })

  it('should display category cards on homepage', () => {
    cy.get('.main-content').should('exist')
    cy.get('.info-card .item').should('exist')
    cy.get('.item').contains('Object-Oriented Programming (OOP)').should('be.visible')
  })

  it('should navigate to cards view when clicking a category', () => {
    cy.get('.item').contains('Object-Oriented Programming (OOP)').click()
    cy.url().should('include', '/category/oop')
    cy.get('.category-header').should('exist')
  })

  it('should flip card when clicked', () => {
    cy.get('.item').contains('Object-Oriented Programming (OOP)').click()
    cy.wait(1000)
    cy.get('.flip-card').first().click()
    cy.get('.flip-card.is-flipped').should('exist')
  })

  it('should navigate between cards', () => {
    cy.get('.item').contains('Object-Oriented Programming (OOP)').click()
    cy.wait(1000)
    cy.get('button').contains('Previous')
    cy.get('button').contains('Next')
  })

  it('should return to categories when clicking back', () => {
    cy.get('.item').contains('Object-Oriented Programming (OOP)').click()
    cy.wait(1000)
    cy.get('.back-button').click()
    cy.get('.info-card').should('exist')
  })
})