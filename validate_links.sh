#!/bin/bash

# Function to validate short link → redirect → affiliate
function validate_link() {
  local alias=$1
  local short_link=$2
  local expected_aff_id=$3
  
  # Get final redirect URL
  redirect_info=$(curl -sLI "$short_link" | grep -E "^HTTP|^Location" | tail -n 2)
  
  # Extract final URL and status
  status=$(echo "$redirect_info" | head -n 1 | awk '{print $2}')
  final_url=$(echo "$redirect_info" | tail -n 1 | tr -d "\r")
  
  # Check if URL contains affiliateId
  if [[ "$final_url" == *"affiliateId="* ]]; then
    real_aff_id=$(echo "$final_url" | grep -oE "affiliateId=[^&]+" | cut -d'=' -f2)
    aff_match="❌ NO"
    [[ "$real_aff_id" == "$expected_aff_id" ]] && aff_match="✅ YES"
  else
    aff_match="❌ MISSING"
    real_aff_id="N/A"
  fi
  
  # Print format
  printf "| %-20s | %-35s | %-50s | %-6s | %-7s |\n" "$alias" "$short_link" "${final_url:0:50}..." "$status" "$aff_match"
}

# Expected affiliate ID
AFF_ID="23619984"  # Official Shopee Affiliate ID for @alwayscuanbos

# Header
printf "| %-20s | %-35s | %-50s | %-6s | %-7s |\n" "Link Alias" "Short Link" "Real URL" "Status" "Match?"
printf "|----------------------|-------------------------------------|----------------------------------------------------|--------|---------|\n"

# Validate existing links from routing plan
validate_link "Viral-Hot-Items" "https://ho.link/racun-shopee-viral" "$AFF_ID"
validate_link "Diskon-Hunter" "https://ho.link/racun-diskon-hunter" "$AFF_ID"
validate_link "Racun-Herbal" "https://ho.link/racun-herbal" "$AFF_ID"
validate_link "Racun-Sultan" "https://ho.link/racun-sultan" "$AFF_ID"
validate_link "Racun-Family" "https://ho.link/racun-family" "$AFF_ID"
validate_link "Hot-Item-24-Hrs" "https://ho.link/racun-stok-terbatas" "$AFF_ID"
validate_link "Sultan-Emak-Review" "https://ho.link/review-sultan-emak" "$AFF_ID"
validate_link "Diskon-90-Persen" "https://ho.link/racun-diskon-90" "$AFF_ID"
validate_link "Produk-Sehat" "https://ho.link/racun-sehat" "$AFF_ID"
validate_link "Fashion-Viral" "https://ho.link/racun-fashion-viral" "$AFF_ID"
validate_link "Gadget-Viral" "https://ho.link/racun-gadget-viral" "$AFF_ID"
validate_link "Kuliner-Hits" "https://ho.link/racun-kuliner" "$AFF_ID"
validate_link "Beauty-Trending" "https://ho.link/racun-beauty" "$AFF_ID"
validate_link "Home-Living" "https://ho.link/racun-home-living" "$AFF_ID"
validate_link "Parenting-Pro" "https://ho.link/racun-parenting" "$AFF_ID"
validate_link "Elektronik-Viral" "https://ho.link/racun-elektronik" "$AFF_ID"
validate_link "Olahraga-Trending" "https://ho.link/racun-sports" "$AFF_ID"
validate_link "Office-Tools" "https://ho.link/racun-office" "$AFF_ID"
validate_link "Hobi-Trending" "https://ho.link/racun-hobi" "$AFF_ID"
validate_link "Baby-Necessities" "https://ho.link/racun-baby" "$AFF_ID"
validate_link "Promo-4.5M" "https://ho.link/korban-juni" "$AFF_ID"
validate_link "Flash-Sale" "https://ho.link/flash-sale-today" "$AFF_ID"
validate_link "Best-Seller" "https://ho.link/best-seller-maret" "$AFF_ID"
validate_link "Brand-Lokal" "https://ho.link/brand-lokal-indo" "$AFF_ID"