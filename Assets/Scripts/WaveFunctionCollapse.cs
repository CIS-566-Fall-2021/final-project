using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;

class Board
{
    public Dictionary<Vector3Int, List<TileBase>> superpositions;

    public Board()
    {
        superpositions = new Dictionary<Vector3Int, List<TileBase>>();
    }

    public Board(Board other)
    {
        superpositions = new Dictionary<Vector3Int, List<TileBase>>();
        foreach (Vector3Int t in other.superpositions.Keys)
        {
            superpositions.Add(t, new List<TileBase>(other.superpositions[t]));
        }
    }

    // not used
    public override int GetHashCode()
    {
        int hashCode = 0;
        foreach (Vector3Int tile in superpositions.Keys)
        {
            if (superpositions[tile].Count == 1)
            {
                hashCode += superpositions[tile][0].GetHashCode();
            }
        }
        return hashCode;
    }

    public override bool Equals(object obj) 
    { 
        var other = obj as Board;
        if (other == null) {
            return false;
        }

        foreach (Vector3Int tile in superpositions.Keys)
        {
            if (other.superpositions.ContainsKey(tile))
            {
                if (superpositions[tile].Count == 1 && other.superpositions[tile].Count == 1)
                {
                    if (!superpositions[tile][0].Equals(other.superpositions[tile][0]))
                    {
                        return false;
                    }
                }
            }
            else
            {
                return false;
            }
        }

        return true;
    }
}

public class WaveFunctionCollapse : MonoBehaviour
{
    public int maxIterations = 1000;

    private bool weighted = true;

    private bool drawOutput = false;

    [SerializeField]
    InputManager inputManager;

    private enum Direction {Left, Right, Up, Down};

    [SerializeField]
    private List<TileBase> seenTiles;

    [SerializeField]
    private Tilemap input;

    [SerializeField]
    private Tilemap output;

    [SerializeField]
    private Tilemap outputDraw;
    
    [SerializeField]
    private TileBase fallbackTile;

    private Dictionary<TileBase, Dictionary<Direction, HashSet<TileBase>>> tileConstraints;
    private Dictionary<TileBase, int> tileWeights;
    private Board board;
    private List<Vector3Int> setTiles;
    // private HashSet<Board> boardBlacklist;
    private Stack<Board> history;
    private Stack<List<Vector3Int>> setHistory;

    private BoundsInt inputBounds;
    private BoundsInt outputBounds;
    private bool firstTile = false;
    private bool running = false;



    // Start is called before the first frame update
    void Start()
    {
        if (input != null && output != null && fallbackTile != null)
        {
            StartWFC();
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

    public void StartWFC()
    {
        if (!running)
        {
            running = true;
            StartCoroutine("RunWFC");
        }
    }

    IEnumerator RunWFC()
    {
        float startTime = Time.time;
        InitializeConstraints();

        if(!InitializeWFC())
        {
            int i = 0;
            while (!IsBoardConverged() && i < maxIterations)
            {
                yield return new WaitUntil(PerformWFC);
                i++;
            }

            bool converged = IsBoardConverged();
            Debug.Log("Iterations: " + i);
            Debug.Log("Converged: " + converged);

            if (i >= maxIterations && !converged)
            {
                inputManager.ShowError("Could not fix conflicts! Change the input tilemap.");
            }

            Debug.Log("Time Elapsed: " + (Time.time - startTime));
        }
        else
        {
            inputManager.ShowError("Starting output has conflicts!");
        }
        firstTile = false;
        yield return null;
        running = false;
        inputManager.ToggleInput(true);
    }

    void InitializeConstraints()
    {
        tileWeights = new Dictionary<TileBase, int>();
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
                    if (!tileWeights.ContainsKey(tile))
                    {
                        tileWeights.Add(tile, 1);
                    }
                    else
                    {
                        tileWeights[tile] += 1;
                    }
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

    bool InitializeWFC()
    {
        // boardBlacklist = new HashSet<Board>();
        history = new Stack<Board>();
        setHistory = new Stack<List<Vector3Int>>();
        board = new Board();
        output.CompressBounds();
        outputBounds = output.cellBounds;
        int z = output.origin.z;
        seenTiles = new List<TileBase>(tileConstraints.Keys);
        // initialize set of possible tiles for every tile
        List<Vector3Int> drawnTiles = new List<Vector3Int>();
        for (int x = outputBounds.min.x; x < outputBounds.max.x; x++) 
        {
            for (int y = outputBounds.min.y; y < outputBounds.max.y; y++) 
            {
                if (!drawOutput)
                {
                    output.SetTile(new Vector3Int(x, y, z), fallbackTile);
                    Dictionary<TileBase, TileBase> tileset = new Dictionary<TileBase, TileBase>();
                    foreach (TileBase tile in seenTiles)
                    {
                        if (!tileset.ContainsKey(tile))
                        {
                            tileset.Add(tile, tile);
                        }
                    }
                    board.superpositions.Add(new Vector3Int(x, y, z), new List<TileBase>(tileset.Keys));
                }
                else
                {
                    TileBase drawTile = outputDraw.GetTile(new Vector3Int(x, y, z));
                    if (drawTile != null)
                    {
                        Vector3Int pos = new Vector3Int(x, y, z);
                        output.SetTile(pos, drawTile);
                        List<TileBase> temp = new List<TileBase>();
                        temp.Add(drawTile);
                        output.SetTile(pos, drawTile);
                        board.superpositions.Add(pos, temp);
                        drawnTiles.Add(pos);
                    }
                    else
                    {
                        output.SetTile(new Vector3Int(x, y, z), fallbackTile);
                        Dictionary<TileBase, TileBase> tileset = new Dictionary<TileBase, TileBase>();
                        foreach (TileBase tile in seenTiles)
                        {
                            if (!tileset.ContainsKey(tile))
                            {
                                tileset.Add(tile, tile);
                            }
                        }
                        board.superpositions.Add(new Vector3Int(x, y, z), new List<TileBase>(tileset.Keys));
                    }
                }
            }
        }
        setTiles = new List<Vector3Int>(board.superpositions.Keys);
        if (drawOutput && drawnTiles.Count > 0)
        {
            firstTile = true;
            foreach (Vector3Int drawnTile in drawnTiles)
            {
                setTiles.Remove(drawnTile);
            }
            AddDrawnConstraints(drawnTiles);
            if (RemoveStartSuperpositions(drawnTiles))
            {
                return true;
            }
        }
        // backup board state and tiles we've set randomly, in case there is a conflict
        Backup();
        return false;
    }

    void AddDrawnConstraints(List<Vector3Int> tiles)
    {
        foreach (Vector3Int t in tiles)
        {
            TileBase tile = output.GetTile(t);
            if (tile != null) 
            {
                if (!tileWeights.ContainsKey(tile))
                {
                    tileWeights.Add(tile, 1);
                }
                else
                {
                    tileWeights[tile] += 1;
                }
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
                TileBase leftN = output.GetTile(new Vector3Int(t.x - 1, t.y, t.z));
                TileBase rightN = output.GetTile(new Vector3Int(t.x + 1, t.y, t.z));
                TileBase upN = output.GetTile(new Vector3Int(t.x, t.y + 1, t.z));
                TileBase downN = output.GetTile(new Vector3Int(t.x, t.y - 1, t.z));

                if (leftN != null && leftN != fallbackTile)
                {
                    neighbors[Direction.Left].Add(leftN);
                }
                if (rightN != null && rightN != fallbackTile)
                {
                    neighbors[Direction.Right].Add(rightN);
                }
                if (upN != null && upN != fallbackTile)
                {
                    neighbors[Direction.Up].Add(upN);
                }
                if (downN != null && downN != fallbackTile)
                {
                    neighbors[Direction.Down].Add(downN);
                }
            }
        }
    }

    bool RemoveStartSuperpositions(List<Vector3Int> tiles)
    {
        Queue<Vector3Int> tilesToEnforce = new Queue<Vector3Int>(tiles);
        bool conflict = false;
        while (tilesToEnforce.Count > 0)
        {
            List<Vector3Int> neighbors = RemoveIllegalTiles(tilesToEnforce.Dequeue());
            foreach (Vector3Int t in neighbors)
            {
                if (board.superpositions[t].Count == 0)
                {
                    conflict = true;
                    break;
                }
                tilesToEnforce.Enqueue(t);
            }
            if (conflict)
            {
                break;
            }
        }
        return conflict;
    }

    void Backup()
    {
        history.Push(new Board(board));
        setHistory.Push(new List<Vector3Int>(setTiles));
    }

    void Reload()
    {
        board = history.Pop();
        setTiles = setHistory.Pop();
    }

    // bool PerformWFC()
    // {
    //     // get random non converged tile
    //     Vector3Int tile = GetRandomTile();

    //     // set tile to random tile
    //     List<TileBase> tiles = new List<TileBase>(board.superpositions[tile]);
    //     bool normal = false;
    //     while (tiles.Count > 0)
    //     {
    //         int rand = Random.Range(0, tiles.Count);
    //         TileBase tileToSet = tiles[rand];
    //         output.SetTile(tile, tileToSet);
    //         output.RefreshTile(tile);
    //         // set superposition to set tile
    //         board.superpositions[tile].Clear();
    //         board.superpositions[tile].Add(tileToSet);
    //         setTiles.Remove(tile);
    //         tiles.Remove(tileToSet);

    //         // propagate removal of invalid tiles from neighbors
    //         Queue<Vector3Int> tilesToEnforce = new Queue<Vector3Int>();
    //         tilesToEnforce.Enqueue(tile);
    //         bool conflict = false;
    //         while (tilesToEnforce.Count > 0)
    //         {
    //             List<Vector3Int> neighbors = RemoveIllegalTiles(tilesToEnforce.Dequeue());
    //             foreach (Vector3Int t in neighbors)
    //             {
    //                 if (board.superpositions[t].Count == 0)
    //                 {
    //                     conflict = true;
    //                     break;
    //                 }
    //                 tilesToEnforce.Enqueue(t);
    //             }
    //             if (conflict)
    //             {
    //                 Reload();
    //                 Backup();
    //                 break;
    //             }
    //         }
    //         if (!conflict)
    //         {
    //             if (boardBlacklist.Contains(board))
    //             {
    //                 Debug.Log("set works");
    //                 Reload();
    //                 Backup();
    //             }
    //             else
    //             {
    //                 normal = true;
    //                 Backup();
    //                 break;
    //             }
    //         }
    //     }

    //     if (!normal)
    //     {
    //         Reload();
            
    //         Debug.Log("adding to blacklist: " + boardBlacklist.Add(board));
    //         Reload();
    //         Backup();
    //     }
        
    //     return true;
    // }

    bool PerformWFC()
    {
        // get random non converged tile
        Vector3Int tile = GetRandomTile();

        // set tile to random tile
        List<TileBase> tiles = board.superpositions[tile];

        int weights = 0;
        foreach (TileBase t in tiles)
        {
            weights += tileWeights[t];
        }
        int rand = Random.Range(0, tiles.Count);
        TileBase tileToSet = tiles[rand];
        if (weighted)
        {
            rand = Random.Range(0, weights);
            int weight = 0;
            foreach (TileBase t in tiles)
            {
                weight += tileWeights[t];
                if (rand < weight)
                {
                    tileToSet = t;
                    break;
                }
            }
        }
        output.SetTile(tile, tileToSet);
        output.RefreshTile(tile);
        // set superposition to set tile
        board.superpositions[tile].Clear();
        board.superpositions[tile].Add(tileToSet);
        setTiles.Remove(tile);

        // propagate removal of invalid tiles from neighbors
        Queue<Vector3Int> tilesToEnforce = new Queue<Vector3Int>();
        tilesToEnforce.Enqueue(tile);
        bool conflict = false;
        while (tilesToEnforce.Count > 0)
        {
            List<Vector3Int> neighbors = RemoveIllegalTiles(tilesToEnforce.Dequeue());
            foreach (Vector3Int t in neighbors)
            {
                if (board.superpositions[t].Count == 0)
                {
                    conflict = true;
                    break;
                }
                tilesToEnforce.Enqueue(t);
            }
            if (conflict)
            {
                for (int i = 0; i < history.Count / 2; i++)
                {
                    Reload();
                }
                Backup();
                break;
            }
        }
        if (!conflict)
        {
            Backup();
        }
        
        return true;
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
        foreach (TileBase t in board.superpositions[tile])
        {
            lVal.UnionWith(tileConstraints[t][Direction.Left]);
            rVal.UnionWith(tileConstraints[t][Direction.Right]);
            uVal.UnionWith(tileConstraints[t][Direction.Up]);
            dVal.UnionWith(tileConstraints[t][Direction.Down]);
        }
        // iterate through superpositions in each neighbor and remove tiles not in legal set
        if (board.superpositions.ContainsKey(left))
        {
            if (RemoveTilesFromSuperposition(new List<TileBase>(board.superpositions[left]), left, lVal))
            {
                modifiedNeighbors.Add(left);
            }
        }
        if (board.superpositions.ContainsKey(right))
        {
            if (RemoveTilesFromSuperposition(new List<TileBase>(board.superpositions[right]), right, rVal))
            {
                modifiedNeighbors.Add(right);
            }
        }
        if (board.superpositions.ContainsKey(up))
        {
            if (RemoveTilesFromSuperposition(new List<TileBase>(board.superpositions[up]), up, uVal))
            {
                modifiedNeighbors.Add(up);
            }
        }
        if (board.superpositions.ContainsKey(down))
        {
            if (RemoveTilesFromSuperposition(new List<TileBase>(board.superpositions[down]), down, dVal))
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
                board.superpositions[tile].Remove(t);
            }
        }
        if (board.superpositions[tile].Count <= 1)
        {
            if (board.superpositions[tile].Count == 1)
            {
                output.SetTile(tile, board.superpositions[tile][0]);
                output.RefreshTile(tile);
            }
            setTiles.Remove(tile);
        }
        return modified;
    }

    Vector3Int GetRandomTile()
    {
        if (!firstTile)
        {
            firstTile = true;
            int rand = Random.Range(0, setTiles.Count);
            Vector3Int randTile = setTiles[rand];
            return randTile;
        }
        else
        {
            Vector3Int randTile = GetLowestEntropy();
            return randTile;
        }
    }

    Vector3Int GetLowestEntropy()
    {
        int entropy = int.MaxValue;
        List<Vector3Int> lowestEntropy = new List<Vector3Int>();
        foreach (Vector3Int tile in setTiles)
        {
            if (board.superpositions[tile].Count < entropy)
            {
                entropy = board.superpositions[tile].Count;
                lowestEntropy.Clear();
                lowestEntropy.Add(tile);
            }
            else if (board.superpositions[tile].Count == entropy)
            {
                lowestEntropy.Add(tile);
            }
        }
        int rand = Random.Range(0, lowestEntropy.Count);
        return lowestEntropy[rand];
    }

    bool IsConverged(Vector3Int tile)
    {
        return board.superpositions[tile].Count <= 1;
    }

    bool IsBoardConverged()
    {
        foreach (List<TileBase> tiles in board.superpositions.Values)
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
        foreach (Vector3Int t in board.superpositions.Keys)
        {
            List<TileBase> tile = board.superpositions[t];
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

    public void SetWeighted()
    {
        weighted = !weighted;
    }

    public void SetDrawOutput()
    {
        drawOutput = !drawOutput;
    }

    public void SetInputTilemap(Tilemap i)
    {
        if (!running)
        {
            input = i;
        }
    }

    public void ClearOutput()
    {
        int z = output.origin.z;
        for (int x = outputBounds.min.x; x < outputBounds.max.x; x++) 
        {
            for (int y = outputBounds.min.y; y < outputBounds.max.y; y++) 
            {
                output.SetTile(new Vector3Int(x, y, z), fallbackTile);
            }
        }
    }
}
