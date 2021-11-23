using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;

public class WaveFunctionCollapse : MonoBehaviour
{
    public int maxIterations = 1000;
    private enum Direction {Left, Right, Up, Down};

    [SerializeField]
    private List<TileBase> seenTiles;

    [SerializeField]
    private Tilemap input;

    [SerializeField]
    private Tilemap output;
    
    [SerializeField]
    private TileBase fallbackTile;

    private Dictionary<TileBase, Dictionary<Direction, HashSet<TileBase>>> tileConstraints;

    private Dictionary<Vector3Int, Dictionary<TileBase, TileBase>> superpositions;
    private List<Vector3Int> setTiles;

    private BoundsInt inputBounds;
    private BoundsInt outputBounds;


    // Start is called before the first frame update
    void Start()
    {
        if (input != null && output != null && fallbackTile != null)
        {
            InitializeConstraints();

            InitializeWFC();

            int i = 0;
            while (!IsBoardConverged() && i < maxIterations)
            {
                PerformWFC();
                i++;
            }
            Debug.Log("Iterations: " + i);
            Debug.Log("Converged: " + IsBoardConverged());

            SetAllTiles();

            output.RefreshAllTiles();
        }
        else
        {
            if (input == null)
            {
                Debug.LogError("Input tilemap not set!");
            }
            if (output == null)
            {
                Debug.LogError("Output tilemap not set!");
            }
            if (fallbackTile == null)
            {
                Debug.LogError("Fallback tile not set!");
            }
        }
    }

    void InitializeConstraints()
    {
        tileConstraints = new Dictionary<TileBase, Dictionary<Direction, HashSet<TileBase>>>();
        input.CompressBounds();
        int z = input.origin.z;
        inputBounds = input.cellBounds;
        // iterate through tilemap and create tile constraints
        for (int x = inputBounds.min.x; x < inputBounds.max.x; x++) 
        {
            for (int y = inputBounds.min.y; y < inputBounds.max.y; y++) 
            {
                TileBase tile = input.GetTile(new Vector3Int(x, y, z));
                if (tile != null) 
                {
                    if (!tileConstraints.ContainsKey(tile))
                    {
                        Dictionary<Direction, HashSet<TileBase>> nDict = new Dictionary<Direction, HashSet<TileBase>>();
                        nDict.Add(Direction.Left, new HashSet<TileBase>());
                        nDict.Add(Direction.Right, new HashSet<TileBase>());
                        nDict.Add(Direction.Up, new HashSet<TileBase>());
                        nDict.Add(Direction.Down, new HashSet<TileBase>());
                        tileConstraints.Add(tile, nDict);
                    }

                    // look at neighbors and fill in legal neighbor set
                    Dictionary<Direction, HashSet<TileBase>> neighbors = tileConstraints[tile];
                    TileBase leftN = input.GetTile(new Vector3Int(x - 1, y, z));
                    TileBase rightN = input.GetTile(new Vector3Int(x + 1, y, z));
                    TileBase upN = input.GetTile(new Vector3Int(x, y + 1, z));
                    TileBase downN = input.GetTile(new Vector3Int(x, y - 1, z));

                    if (leftN != null)
                    {
                        neighbors[Direction.Left].Add(leftN);
                    }
                    if (rightN != null)
                    {
                        neighbors[Direction.Right].Add(rightN);
                    }
                    if (upN != null)
                    {
                        neighbors[Direction.Up].Add(upN);
                    }
                    if (downN != null)
                    {
                        neighbors[Direction.Down].Add(downN);
                    }
                }
            }
        }
    }

    void InitializeWFC()
    {
        superpositions = new Dictionary<Vector3Int, Dictionary<TileBase, TileBase>>();
        output.CompressBounds();
        outputBounds = output.cellBounds;
        int z = output.origin.z;
        seenTiles = new List<TileBase>(tileConstraints.Keys);
        // initialize set of possible tiles for every tile
        for (int x = outputBounds.min.x; x < outputBounds.max.x; x++) 
        {
            for (int y = outputBounds.min.y; y < outputBounds.max.y; y++) 
            {

                Dictionary<TileBase, TileBase> tileset = new Dictionary<TileBase, TileBase>();
                foreach (TileBase tile in seenTiles)
                {
                    if (!tileset.ContainsKey(tile))
                    {
                        tileset.Add(tile, tile);
                    }
                }
                superpositions.Add(new Vector3Int(x, y, z), tileset);
            }
        }
        setTiles = new List<Vector3Int>(superpositions.Keys);
    }

    void PerformWFC()
    {
        // get random non converged tile
        Vector3Int tile = GetRandomTile();

        // set tile to random tile
        List<TileBase> tiles = new List<TileBase>(superpositions[tile].Keys);
        int rand = Random.Range(0, tiles.Count);
        TileBase tileToSet = tiles[rand];
        output.SetTile(tile, tileToSet);
        output.RefreshTile(tile);
        // set superposition to set tile
        superpositions[tile].Clear();
        superpositions[tile].Add(tileToSet, tileToSet);

        // propagate removal of invalid tiles from neighbors
        Queue<Vector3Int> tilesToEnforce = new Queue<Vector3Int>();
        tilesToEnforce.Enqueue(tile);
        while (tilesToEnforce.Count > 0)
        {
            List<Vector3Int> neighbors = RemoveIllegalTiles(tilesToEnforce.Dequeue());
            foreach (Vector3Int t in neighbors)
            {
                tilesToEnforce.Enqueue(t);
            }
        }
    }

    List<Vector3Int> RemoveIllegalTiles(Vector3Int tile)
    {
        // tells which neighbors have been modified
        List<Vector3Int> modifiedNeighbors = new List<Vector3Int>();

        Vector3Int left = new Vector3Int(tile.x - 1, tile.y, tile.z);
        Vector3Int right = new Vector3Int(tile.x + 1, tile.y, tile.z);
        Vector3Int up = new Vector3Int(tile.x, tile.y + 1, tile.z);
        Vector3Int down = new Vector3Int(tile.x, tile.y - 1, tile.z);
        HashSet<TileBase> lVal = new HashSet<TileBase>();
        HashSet<TileBase> rVal = new HashSet<TileBase>();
        HashSet<TileBase> uVal = new HashSet<TileBase>();
        HashSet<TileBase> dVal = new HashSet<TileBase>();
        foreach (TileBase t in superpositions[tile].Keys)
        {
            lVal.UnionWith(tileConstraints[t][Direction.Left]);
            rVal.UnionWith(tileConstraints[t][Direction.Right]);
            uVal.UnionWith(tileConstraints[t][Direction.Up]);
            dVal.UnionWith(tileConstraints[t][Direction.Down]);
        }
        // iterate through superpositions in each neighbor and remove tiles not in legal set
        if (superpositions.ContainsKey(left))
        {
            if (RemoveTilesFromSuperposition(new List<TileBase>(superpositions[left].Keys), left, lVal))
            {
                modifiedNeighbors.Add(left);
            }
        }
        if (superpositions.ContainsKey(right))
        {
            if (RemoveTilesFromSuperposition(new List<TileBase>(superpositions[right].Keys), right, rVal))
            {
                modifiedNeighbors.Add(right);
            }
        }
        if (superpositions.ContainsKey(up))
        {
            if (RemoveTilesFromSuperposition(new List<TileBase>(superpositions[up].Keys), up, uVal))
            {
                modifiedNeighbors.Add(up);
            }
        }
        if (superpositions.ContainsKey(down))
        {
            if (RemoveTilesFromSuperposition(new List<TileBase>(superpositions[down].Keys), down, dVal))
            {
                modifiedNeighbors.Add(down);
            }
        }
        return modifiedNeighbors;
    }

    bool RemoveTilesFromSuperposition(List<TileBase> tiles, Vector3Int tile, HashSet<TileBase> valid)
    {
        bool modified = false;
        foreach (TileBase t in tiles)
        {
            if (!valid.Contains(t))
            {
                modified = true;
                superpositions[tile].Remove(t);
            }
        }
        return modified;
    }

    Vector3Int GetRandomTile()
    {
        int rand = Random.Range(0, setTiles.Count);
        Vector3Int randTile = setTiles[rand];
        setTiles.RemoveAt(rand);
        return randTile;
    }

    bool IsConverged(Vector3Int tile)
    {
        return superpositions[tile].Count <= 1;
    }

    bool IsBoardConverged()
    {
        foreach (Dictionary<TileBase, TileBase> tiles in superpositions.Values)
        {
            if (tiles.Count > 1)
            {
                return false;
            }
        }
        return true;
    }

    void SetAllTiles()
    {
        foreach (Vector3Int t in superpositions.Keys)
        {
            List<TileBase> tile = new List<TileBase>(superpositions[t].Keys);
            if (tile.Count == 0)
            {
                output.SetTile(t, fallbackTile);
            }
            else if (tile.Count == 1)
            {
                output.SetTile(t, tile[0]);
            }
        }
    }
}
