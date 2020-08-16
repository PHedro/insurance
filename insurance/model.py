from tabulate import tabulate

from insurance.file_handler import csv_from_file, json_from_file


class Contract:
    def __init__(self, contract_data):
        self.max_amount = contract_data.get("MaxAmount", 0)
        for item in contract_data.get("Coverage", []):
            _attr = item.get("Attribute").lower()
            _include_value = item.get("Include", set())
            _exclude_value = item.get("Exclude", set())
            setattr(self, f"{_attr}_include", set(_include_value))
            setattr(self, f"{_attr}_exclude", set(_exclude_value))

    def _check_value(self, _attribute, _value):
        _included = getattr(self, f"{_attribute}_include", set())
        _excluded = getattr(self, f"{_attribute}_exclude", set())

        is_included = True if not _included else _value in _included
        is_excluded = False if not _excluded else _value in _excluded
        return is_included and not is_excluded

    def location_allowed(self, value):
        return self._check_value(_attribute="location", _value=value)

    def peril_allowed(self, value):
        return self._check_value(_attribute="peril", _value=value)

    def event_loss_reimbursement(self, event):
        return event.loss if event.loss < self.max_amount else self.max_amount


class Deal:
    HEADERS = ["DealId", "Company", "Peril", "Location"]

    def __init__(self, deal_id, company, peril, location):
        self.deal_id = int(deal_id)
        self.company = company
        self.peril = peril
        self.location = location

    @staticmethod
    def as_tuples(deals):
        return sorted([deal.to_tuple() for deal in deals], key=lambda item: item[0])

    def to_tuple(self):
        return self.deal_id, self.company, self.peril, self.location

    def is_covered(self, contract):
        location_included = contract.location_allowed(value=self.location)
        peril_included = contract.peril_allowed(value=self.peril)
        return location_included and peril_included


class Event:
    def __init__(self, event_id, deal_id, loss):
        self.event_id = int(event_id)
        self.deal_id = int(deal_id)
        self.loss = int(loss)


class Insurance:
    def __init__(self, contract_path, deals_csv, event_losses_csv):
        self.contract = Contract(contract_data=json_from_file(contract_path))
        self.deals = self.covered_deals(deals_csv=deals_csv)
        self.sum_losses_by_peril = self.reimbursement_losses_by_peril(
            event_losses_csv=event_losses_csv
        )

    def covered_deals(self, deals_csv):
        return {
            deal.deal_id: deal
            for deal in [Deal(*_deal) for _deal in csv_from_file(deals_csv)[1:]]
            if deal.is_covered(contract=self.contract)
        }

    def reimbursement_losses_by_peril(self, event_losses_csv):
        losses_by_peril = {}
        deals_covered_ids = self.deals.keys()
        for _event in csv_from_file(event_losses_csv)[1:]:
            event = Event(*_event)
            if event.deal_id in deals_covered_ids:
                _deal = self.deals.get(event.deal_id)
                _events = losses_by_peril.get(_deal.peril, [])
                _events.append(self.contract.event_loss_reimbursement(event))
                losses_by_peril.update({_deal.peril: _events})

        return {key: sum(value) for key, value in losses_by_peril.items()}

    def print_covered_deals(self):
        print(tabulate(Deal.as_tuples(self.deals.values()), headers=Deal.HEADERS))

    def print_losses_by_peril(self):
        print(
            tabulate(
                sorted(self.sum_losses_by_peril.items(), key=lambda item: item[0]),
                headers=("Peril", "Loss"),
            )
        )
