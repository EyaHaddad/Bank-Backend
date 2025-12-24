"""Beneficiary services module for beneficiary-related operations."""

import logging
from uuid import UUID

from sqlalchemy.orm import Session

from . import schemas
from .exceptions import (
    BeneficiaryNotFoundError,
    BeneficiaryAccessDeniedError,
    DuplicateBeneficiaryError,
)
from src.models.beneficiary import Beneficiary
from src.models.transfer import Transfer

logger = logging.getLogger(__name__)


class BeneficiaryService:
    """Service class for beneficiary-related operations."""

    def __init__(self, session: Session):
        """Initialize the service with a database session."""
        self._db = session

    def _get_beneficiary(self, beneficiary_id: UUID) -> Beneficiary:
        """Retrieve a beneficiary by its ID."""
        beneficiary = self._db.query(Beneficiary).filter(Beneficiary.id == beneficiary_id).first()
        if not beneficiary:
            raise BeneficiaryNotFoundError(beneficiary_id)
        return beneficiary

    def _validate_ownership(self, beneficiary: Beneficiary, user_id: UUID) -> None:
        """Validate that the user owns the beneficiary."""
        if beneficiary.user_id != user_id:
            raise BeneficiaryAccessDeniedError()

    def _check_duplicate_iban(self, user_id: UUID, iban: str, exclude_id: UUID = None) -> None:
        """Check if a beneficiary with the same IBAN already exists for this user."""
        query = self._db.query(Beneficiary).filter(
            Beneficiary.user_id == user_id,
            Beneficiary.iban == iban,
        )
        if exclude_id:
            query = query.filter(Beneficiary.id != exclude_id)
        if query.first():
            raise DuplicateBeneficiaryError(iban)

    def create_beneficiary(self, user_id: UUID, request: schemas.BeneficiaryCreate) -> schemas.BeneficiaryResponse:
        """Create a new beneficiary for a user."""
        logger.info(f"Creating beneficiary for user {user_id}")

        # Check for duplicate IBAN
        self._check_duplicate_iban(user_id, request.iban)

        beneficiary = Beneficiary(
            user_id=user_id,
            name=request.name,
            bank_name=request.bank_name,
            iban=request.iban,
            email=request.email,
            is_verified=False,  # Beneficiaries need to be verified before use
        )
        self._db.add(beneficiary)
        self._db.commit()
        self._db.refresh(beneficiary)

        logger.info(f"Beneficiary {beneficiary.id} created successfully")
        return schemas.BeneficiaryResponse.model_validate(beneficiary)

    def get_beneficiary(self, beneficiary_id: UUID, user_id: UUID) -> schemas.BeneficiaryResponse:
        """Get a beneficiary ensuring it belongs to the user."""
        beneficiary = self._get_beneficiary(beneficiary_id)
        self._validate_ownership(beneficiary, user_id)
        return schemas.BeneficiaryResponse.model_validate(beneficiary)

    def list_beneficiaries(self, user_id: UUID, verified_only: bool = False) -> schemas.BeneficiaryListResponse:
        """List all beneficiaries for a user."""
        query = self._db.query(Beneficiary).filter(Beneficiary.user_id == user_id)
        
        if verified_only:
            query = query.filter(Beneficiary.is_verified == True)
        
        beneficiaries = query.order_by(Beneficiary.name).all()
        
        return schemas.BeneficiaryListResponse(
            beneficiaries=[schemas.BeneficiaryResponse.model_validate(b) for b in beneficiaries],
            total=len(beneficiaries),
        )

    def update_beneficiary(
        self, beneficiary_id: UUID, user_id: UUID, request: schemas.BeneficiaryUpdate
    ) -> schemas.BeneficiaryResponse:
        """Update a beneficiary."""
        beneficiary = self._get_beneficiary(beneficiary_id)
        self._validate_ownership(beneficiary, user_id)

        if request.name is not None:
            beneficiary.name = request.name
        if request.bank_name is not None:
            beneficiary.bank_name = request.bank_name
        if request.email is not None:
            beneficiary.email = request.email

        # Note: If critical fields are updated, you might want to reset is_verified
        self._db.commit()
        self._db.refresh(beneficiary)

        logger.info(f"Beneficiary {beneficiary_id} updated successfully")
        return schemas.BeneficiaryResponse.model_validate(beneficiary)

    def delete_beneficiary(self, beneficiary_id: UUID, user_id: UUID) -> bool:
        """Delete a beneficiary."""
        beneficiary = self._get_beneficiary(beneficiary_id)
        self._validate_ownership(beneficiary, user_id)

        # Check if there are any transfers to this beneficiary
        transfer_count = self._db.query(Transfer).filter(Transfer.beneficiary_id == beneficiary_id).count()
        if transfer_count > 0:
            logger.warning(f"Deleting beneficiary {beneficiary_id} which has {transfer_count} transfers")
            # In production, consider soft delete instead

        self._db.delete(beneficiary)
        self._db.commit()

        logger.info(f"Beneficiary {beneficiary_id} deleted successfully")
        return True

    def verify_beneficiary(self, beneficiary_id: UUID, user_id: UUID) -> schemas.BeneficiaryResponse:
        """
        Verify a beneficiary (mark as verified).
        
        In a real application, this would involve additional verification steps
        like confirming bank details, sending a test transaction, etc.
        """
        beneficiary = self._get_beneficiary(beneficiary_id)
        self._validate_ownership(beneficiary, user_id)

        beneficiary.is_verified = True
        self._db.commit()
        self._db.refresh(beneficiary)

        logger.info(f"Beneficiary {beneficiary_id} verified successfully")
        return schemas.BeneficiaryResponse.model_validate(beneficiary)

    def unverify_beneficiary(self, beneficiary_id: UUID, user_id: UUID) -> schemas.BeneficiaryResponse:
        """
        Unverify a beneficiary (mark as not verified).
        
        This might be needed if beneficiary details change and re-verification is required.
        """
        beneficiary = self._get_beneficiary(beneficiary_id)
        self._validate_ownership(beneficiary, user_id)

        beneficiary.is_verified = False
        self._db.commit()
        self._db.refresh(beneficiary)

        logger.info(f"Beneficiary {beneficiary_id} unverified")
        return schemas.BeneficiaryResponse.model_validate(beneficiary)
