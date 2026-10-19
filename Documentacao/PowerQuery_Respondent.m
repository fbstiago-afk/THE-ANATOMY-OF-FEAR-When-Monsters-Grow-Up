let
    // Same parser as the starter tables: JSON array -> distinct trimmed list (never split on commas).
    Parse = (v as any) as list => if v = null or Text.Trim(Text.From(v)) = "" then {} else let j = Json.Document(v) in if not Value.Is(j, type list) then error "Fear JSON must be a list" else List.Distinct(List.Select(List.Transform(j, each if _ = null then "" else Text.Trim(Text.From(_))), each _ <> "")),
    Clean = (v as any) as text => if v = null or Text.Trim(Text.From(v)) = "" then "(Unknown)" else Text.Trim(Text.From(v)),
    Source = raw_survey_responses,
    Checked = if Table.RowCount(Source) <> List.Count(List.Distinct(Source[ResponseKey])) then error "ResponseKey must be unique" else Source,
    WithLists = Table.AddColumn(Checked, "Lists", each [C = Parse([childhoodFearsJson]), N = Parse([currentFearsJson])]),
    WithKept = Table.AddColumn(WithLists, "FearsKept", each List.Count(List.Intersect({[Lists][C], [Lists][N]})), Int64.Type),
    WithKeptList = Table.AddColumn(WithKept, "KeptFears", each let k = List.Intersect({[Lists][C], [Lists][N]}) in if List.IsEmpty(k) then "none" else Text.Combine(k, ", "), type text),
    WithAge = Table.AddColumn(WithKeptList, "AgeGroup", each Clean([ageGroup]), type text),
    WithChildCount = Table.AddColumn(WithAge, "ChildhoodFearCount", each List.Count([Lists][C]), Int64.Type),
    WithNowCount = Table.AddColumn(WithChildCount, "CurrentFearCount", each List.Count([Lists][N]), Int64.Type),
    // Derived display labels. The original answer stays untouched in dataNightmare.
    WithShort = Table.AddColumn(WithNowCount, "Nightmare", each let t = Clean([dataNightmare]) in if Text.Contains(t, " (") then Text.Trim(Text.BeforeDelimiter(t, " (")) else t, type text),
    WithDetail = Table.AddColumn(WithShort, "NightmareDetail", each let t = Clean([dataNightmare]) in if Text.Contains(t, " (") then Text.Trim(Text.BeforeDelimiter(Text.AfterDelimiter(t, " ("), ")", {0, RelativePosition.FromEnd})) else "", type text),
    Sorted = Table.Sort(WithDetail, {{"FearsKept", Order.Descending}, {"ResponseKey", Order.Ascending}}),
    Indexed = Table.AddIndexColumn(Sorted, "PersonOrder", 1, 1, Int64.Type),
    Result = Table.SelectColumns(Indexed, {"ResponseKey", "dataNightmare", "Nightmare", "NightmareDetail", "AgeGroup", "FearsKept", "KeptFears", "ChildhoodFearCount", "CurrentFearCount", "PersonOrder"}),
    Typed = Table.TransformColumnTypes(Result, {{"ResponseKey", Int64.Type}, {"dataNightmare", type text}})
in
    Typed