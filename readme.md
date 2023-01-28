# Contrat d'interface

<table>

<tr>
<th>ENDPOINT</th>
<th>METHOD</th>
<th>HEADER</th>
<th>QUERY PARAMETER</th>
<th>BODY</th>
<th>RESPONSE</th>
</tr>

<tr>
<td>/masterpieces</td>
<td>GET</td>
<td></td>
<td>user_id<br><strong>optional</strong></td>
<td></td>
<td>

```json
{
  "total": 1,
  "data": [
    {
      "movie_id": 108,
      "movie_name": "Matrix",
      "user_id": 18,
      "user_name": "roberto17"
    }
  ]
}
```

</td>
</tr>

<tr>
<td></td>
<td>POST</td>
<td>Authorization: Bearer <i>token<i/></td>
<td></td>
<td>

```json
{
  "movie_id": 101,
  "movie_name": "Le monde de Némo"
}
```

</td>
<td>

```json
{
  "message": "Movie 101 Le monde de Némo successfully added to Masterpiece."
}
```

</td>
</tr>

<tr>
<td>/watchlists</td>
<td>GET</td>
<td></td>
<td>user_id<br><strong>optional</strong></td>
<td></td>
<td>

```json
{
  "total": 1,
  "data": [
    {
      "movie_id": 254,
      "movie_name": "Alice au pays des merveilles"
    }
  ]
}
```

</td>
</tr>

<tr>
<td></td>
<td>POST</td>
<td>Authorization: Bearer <i>token<i/></td>
<td></td>
<td>

```json
{
  "movie_id": 124,
  "movie_name": "Star Trek"
}
```

</td>
<td>

```json
{
  "message": "Movie 124 Star Trek successfully added to Watchlist."
}
```

</td>
</tr>

<tr>
<td>/votes</td>
<td>GET</td>
<td></td>
<td>user_id<br><strong>optional</strong></td>
<td></td>
<td>

```json
{
    "total": 1,
    "data": [
        {
            "movie_id": 508,
            "movie_name": "Le cercle des poètes disparus",
            "value": 4.5,
            "user_id": 2,
            "user_name": "Robert"
    ]
}
```

</td>
</tr>

<tr>
<td></td>
<td>POST</td>
<td>Authorization: Bearer <i>token<i/></td>
<td></td>
<td>

```json
{
  "movie_id": 503,
  "movie_name": "Inspecteur Gadget",
  "value": 3.0
}
```

</td>
<td>

```json
{
  "message": "Movie 503 Inspecteur Gadget successfully added to Vote."
}
```

</td>
</tr>

<tr>
<td>/critics</td>
<td>GET</td>
<td></td>
<td>user_id<br><strong>optional</strong></td>
<td></td>
<td>

```json
{
    "total": 1,
    "data": [
        {
            "movie_id": 165,
            "movie_name": "Titanic",
            "content": "J'adooooore ce film mais à la fin il meurt."
            "user_id": 2,
            "user_name": "Robert"
        }
    ]
}
```

</td>
</tr>

<tr>
<td></td>
<td>POST</td>
<td>Authorization: Bearer <i>token<i/></td>
<td></td>
<td>

```json
{
  "movie_id": 189,
  "movie_name": "Star Wars: La revanche des Siths",
  "content": "Pas ouf..."
}
```

</td>
<td>

```json
{
  "message": "Movie 189 Star Wars: La revanche des Siths successfully added to Critic."
}
```

</td>
</tr>

</table>
