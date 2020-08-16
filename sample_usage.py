from insurance.model import Insurance


def check_insurance():
    insurance = Insurance(
        contract_path="tests/data/contract.json",
        deals_csv="tests/data/deals.csv",
        event_losses_csv="tests/data/losses.csv",
    )
    insurance.print_covered_deals()

    print("\n")

    insurance.print_losses_by_peril()


if __name__ == "__main__":
    check_insurance()
