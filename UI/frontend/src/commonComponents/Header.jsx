import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import bannerImage from '/src/assets/imgs/Banner.png';

function NavBar() {

    return (
        <Navbar expand="lg" bg="dark" data-bs-theme="dark">
            <Navbar.Toggle aria-controls="navbar-nav" />
            <Navbar.Collapse id="navbar-nav">
                <Nav fill variant="pills">
                    <Nav.Link href="/add/expense">Add Expense</Nav.Link>
                    <Nav.Link href="/add/income">Add Income</Nav.Link>
                    <Nav.Link href="/add/transfer">Add Transfer</Nav.Link>
                    <Nav.Link href="/add/deposit">Add Deposit</Nav.Link>
                    <Nav.Link href="/add/currencyrates">Currency Rates</Nav.Link>
                    <Nav.Link href="/view/acc">View Accounts</Nav.Link>
                    <NavDropdown title="Reports" id="nav-dropdown-reports">
                        <NavDropdown.Item href="/view/reports/table">View Reports Table</NavDropdown.Item>
                        <NavDropdown.Item href="/view/reports/year">View Year Report</NavDropdown.Item>
                    </NavDropdown>
                    <NavDropdown title="Options" id="nav-dropdown-options">
                        <NavDropdown.Item href="/options/db">Database options</NavDropdown.Item>
                        <NavDropdown.Item href="/options/pb">Accounts options</NavDropdown.Item>
                    </NavDropdown>
                    <Nav.Link href="/invest">Invest management</Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
}


function Banner() {
    return (
        <>
            <img style={{width: '100%', height: 'auto', display: 'block'}} className="banner" src={bannerImage} alt="Acc0unt1ng Banner" />
        </>
    )
}

export default function Header() {
    return (
        <header>
            <Banner />
            <NavBar />
        </header>
    );
}