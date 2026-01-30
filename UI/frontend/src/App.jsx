import {
  BrowserRouter as Router,
  Route,
  Routes
} from "react-router-dom";
import ExpensePage from "./pages/Expense";
import IncomePage from "./pages/Income";
import TransferPage from "./pages/Transfer";
import DepositPage from "./pages/Deposit";
import CurrencyPage from "./pages/CurrencyRates";
import BalancePage from "./pages/Balance";
import ReportsPage from "./pages/Reports";
import YearPage from "./pages/YearReport";
import InvestTransactionsPage from "./pages/invest/InvestTransactions";
import InvestStockPricePage from "./pages/invest/InvestStockPrice";
import InvestBalancePage from "./pages/invest/InvestBalance";
import InvestOptionsPage from "./pages/invest/InvestOptions";
import { OptionsDBPage, OptionsPBPage } from "./pages/Options";

export default function RoutesMap() {
  return (
    <Router>
      <Routes>
        <Route path='/add/expense' element={<ExpensePage />} />
        <Route path='/add/income' element={<IncomePage />} />
        <Route path='/add/transfer' element={<TransferPage />} />
        <Route path='/add/deposit' element={<DepositPage />} />
        <Route path='/add/currencyrates' element={<CurrencyPage />} />
        <Route path='/view/acc' element={<BalancePage />} />
        <Route path='/view/reports/table' element={<ReportsPage />} />
        <Route path='/view/reports/year' element={<YearPage />} />
        <Route path='/options/db' element={<OptionsDBPage />} />
        <Route path='/options/pb' element={<OptionsPBPage />} />
        <Route path='/invest/transactions' element={<InvestTransactionsPage />} />
        <Route path='/invest/stockprice' element={<InvestStockPricePage />} />
        <Route path='/invest/balance' element={<InvestBalancePage />} />
        <Route path='/invest/options' element={<InvestOptionsPage />} />
        <Route path='/' element={<ExpensePage />} >
        </Route>
      </Routes>
    </Router>
  );
}
