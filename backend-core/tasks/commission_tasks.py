from celery import shared_task
from django.db import transaction as db_transaction
from commerce.models import Transaction, CommissionLog
import logging

logger = logging.getLogger(__name__)

@shared_task
def calculate_commission(transaction_id):
    """
    Async task to calculate commission for a completed transaction.
    Logic:
    - Total sales > 100,000: 10% commission
    - Total sales <= 100,000: 5% commission
    - Split equally if multiple staff involved.
    """
    logger.info(f"Starting commission calculation for transaction {transaction_id}")
    
    try:
        txn = Transaction.objects.get(id=transaction_id)
        
        # Skip if not completed
        if txn.status != 'COMPLETED':
            logger.warning(f"Transaction {transaction_id} is not COMPLETED. Skipping.")
            return

        # Skip if already calculated
        if hasattr(txn, 'commission_log'):
            logger.info(f"Commission already calculated for {transaction_id}")
            return

        amount = float(txn.total_amount)
        
        # --- Core Business Logic ---
        if amount > 100000:
            rate = 0.10
            rule = "High Value (>100k)"
        else:
            rate = 0.05
            rule = "Standard Value (<=100k)"
            
        total_commission = amount * rate
        
        # Staff Splitting Logic
        staff_members = []
        if txn.staff_1:
            staff_members.append(txn.staff_1)
        if txn.staff_2:
            staff_members.append(txn.staff_2)
            
        if not staff_members:
            logger.warning("No staff assigned to transaction.")
            return

        split_amount = total_commission / len(staff_members)
        
        # Use atomic transaction to ensure logs are created safely
        with db_transaction.atomic():
            for staff in staff_members:
                CommissionLog.objects.create(
                    transaction=txn,
                    staff=staff,
                    amount=split_amount,
                    calculation_details={
                        "rule": rule,
                        "rate": rate,
                        "total_txn_amount": amount,
                        "total_commission_pool": total_commission,
                        "split_count": len(staff_members)
                    }
                )
        
        logger.info(f"Commission calculated successfully for {transaction_id}")
        return f"Calculated: {split_amount} per person ({len(staff_members)})"

    except Transaction.DoesNotExist:
        logger.error(f"Transaction {transaction_id} not found.")
    except Exception as e:
        logger.exception(f"Error calculating commission: {e}")

