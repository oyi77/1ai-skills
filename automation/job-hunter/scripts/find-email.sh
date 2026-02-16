#!/bin/bash
# find-email.sh — Common email pattern checker
# Usage: ./find-email.sh "first" "last" "company.com"

FIRST="$1"
LAST="$2"
DOMAIN="$3"

if [ -z "$FIRST" ] || [ -z "$LAST" ] || [ -z "$DOMAIN" ]; then
    echo "Usage: ./find-email.sh \"first\" \"last\" \"company.com\""
    exit 1
fi

FIRST_LOWER=$(echo "$FIRST" | tr '[:upper:]' '[:lower:]')
LAST_LOWER=$(echo "$LAST" | tr '[:upper:]' '[:lower:]')
FIRST_INITIAL="${FIRST_LOWER:0:1}"
LAST_INITIAL="${LAST_LOWER:0:1}"

echo "🔍 Possible email patterns for $FIRST $LAST @ $DOMAIN"
echo "=============================================="
echo ""
echo "Most common patterns:"
echo "  1. ${FIRST_LOWER}@${DOMAIN}"
echo "  2. ${FIRST_LOWER}.${LAST_LOWER}@${DOMAIN}"
echo "  3. ${FIRST_LOWER}${LAST_LOWER}@${DOMAIN}"
echo "  4. ${FIRST_INITIAL}${LAST_LOWER}@${DOMAIN}"
echo "  5. ${FIRST_INITIAL}.${LAST_LOWER}@${DOMAIN}"
echo "  6. ${FIRST_LOWER}_${LAST_LOWER}@${DOMAIN}"
echo "  7. ${FIRST_LOWER}-${LAST_LOWER}@${DOMAIN}"
echo "  8. ${LAST_LOWER}.${FIRST_LOWER}@${DOMAIN}"
echo "  9. ${LAST_LOWER}${FIRST_INITIAL}@${DOMAIN}"
echo " 10. ${FIRST_LOWER}${LAST_INITIAL}@${DOMAIN}"
echo ""
echo "🔧 Tools to verify:"
echo "  • Hunter.io: hunter.io/email-verifier"
echo "  • NeverBounce: neverbounce.com"
echo "  • Google: \"${FIRST_LOWER} ${LAST_LOWER}\" \"@${DOMAIN}\""
echo ""
echo "💡 Tips:"
echo "  • Check their LinkedIn/Twitter for email in bio"
echo "  • Look at GitHub commits for email"
echo "  • Check company blog author pages"
echo "  • Search: \"${FIRST_LOWER} ${LAST_LOWER}\" email ${DOMAIN}"
