#!/bin/bash
# research-company.sh — Quick company intel gathering
# Usage: ./research-company.sh "Company Name"

COMPANY="$1"

if [ -z "$COMPANY" ]; then
    echo "Usage: ./research-company.sh \"Company Name\""
    exit 1
fi

echo "🔍 Researching: $COMPANY"
echo "================================"
echo ""

echo "📊 General Info:"
echo "   • Search: \"$COMPANY company overview\""
echo "   • Wikipedia: \"$COMPANY\""
echo "   • Crunchbase: crunchbase.com/organization/$(echo $COMPANY | tr '[:upper:]' '[:lower:]' | tr ' ' '-')"
echo ""

echo "💰 Funding & Financials:"
echo "   • Search: \"$COMPANY funding series\""
echo "   • Search: \"$COMPANY valuation\""
echo "   • Crunchbase funding page"
echo ""

echo "⚙️ Tech Stack:"
echo "   • StackShare: stackshare.io/$(echo $COMPANY | tr '[:upper:]' '[:lower:]' | tr ' ' '-')"
echo "   • GitHub: github.com/$(echo $COMPANY | tr '[:upper:]' '[:lower:]' | tr ' ' '-')"
echo "   • Search: \"$COMPANY engineering blog\""
echo "   • Search: \"$COMPANY tech stack\""
echo ""

echo "👥 Culture & Reviews:"
echo "   • Glassdoor: glassdoor.com/Reviews/$COMPANY-Reviews"
echo "   • Blind: teamblind.com/company/$COMPANY"
echo "   • Search: \"$COMPANY culture\""
echo "   • Search: \"$COMPANY interview experience\""
echo ""

echo "📰 Recent News:"
echo "   • Search: \"$COMPANY news 2024 2025\""
echo "   • Search: \"$COMPANY announcement\""
echo "   • Search: \"$COMPANY product launch\""
echo ""

echo "🔗 LinkedIn:"
echo "   • Company page: linkedin.com/company/$(echo $COMPANY | tr '[:upper:]' '[:lower:]' | tr ' ' '-')"
echo "   • Search employees: \"$COMPANY\" + \"recruiter\" or \"engineering manager\""
echo ""

echo "🐦 Twitter/X:"
echo "   • Search: @$COMPANY or $(echo $COMPANY | tr '[:upper:]' '[:lower:]' | tr ' ' '')"
echo "   • Search: \"$COMPANY\" from:@handle"
echo ""

echo "================================"
echo "Use web_search and browser tools to gather this intel."
