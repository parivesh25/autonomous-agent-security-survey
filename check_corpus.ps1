# Read-only audit of the discovery ledger. Run from any directory.
$records = @(Get-Content -LiteralPath (Join-Path $PSScriptRoot 'literature_matrix.json') -Raw | ConvertFrom-Json)
$searches = @(Get-Content -LiteralPath (Join-Path $PSScriptRoot 'search_log.json') -Raw | ConvertFrom-Json)
$titles = @($records | ForEach-Object { $_.title.ToLowerInvariant() -replace '[^a-z0-9]', '' } | Sort-Object -Unique)
$ids = @($records | ForEach-Object { $_.id } | Sort-Object -Unique)
if ($ids.Count -ne $records.Count) { throw 'Duplicate paper record IDs' }
foreach ($s in $searches) {
    $n = @($records | Where-Object search_id -eq $s.search_id).Count
    if ($n -ne $s.returned_count) { throw ('Search count mismatch: ' + $s.search_id) }
}
foreach ($r in $records) {
    if ($r.possible_duplicate_of -and $r.possible_duplicate_of -notin $ids) { throw 'Broken duplicate reference' }
}
[pscustomobject]@{
    returned_records=$records.Count
    distinct_normalized_titles=$titles.Count
    flagged_possible_duplicates=@($records | Where-Object status -eq 'possible_duplicate').Count
    included_records=@($records | Where-Object status -eq 'included').Count
    full_text_read_records=@($records | Where-Object full_text_read -eq $true).Count
    caveat='Normalized titles are not deduplicated works. Included/read counts concern this pilot batch only.'
} | ConvertTo-Json
