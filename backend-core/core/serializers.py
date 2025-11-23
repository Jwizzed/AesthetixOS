from rest_framework import serializers

class PDPAMaskingField(serializers.CharField):
    """
    Custom DRF Field that masks data based on User Role.
    Logic:
    - If User is DOCTOR or ADMIN: Show full data.
    - Else: Mask middle characters.
    """
    
    def to_representation(self, value):
        # value is the actual string from the DB (e.g., "0812345678")
        request = self.context.get('request')
        
        # If no request context or user not authenticated, mask it
        if not request or not request.user.is_authenticated:
            return self.mask_string(value)
            
        try:
            # Check if profile exists safely
            if hasattr(request.user, 'profile'):
                user_role = request.user.profile.role
                if user_role in ['DOCTOR', 'ADMIN']:
                    return value
        except Exception:
            # Fallback if profile access fails
            pass
        
        return self.mask_string(value)

    def mask_string(self, value):
        if not value or len(value) < 6:
            return "*****" # Fallback for short strings
            
        # Mask logic: Keep first 3 and last 4. Mask the middle.
        # e.g. 081-234-5678 -> 081-XXX-5678
        prefix = value[:3]
        suffix = value[-4:]
        return f"{prefix}-XXX-{suffix}"
