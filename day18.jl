function readvault(fname::String)
    # return set of characters in the vault, initial location and map of vault as list of strings
    vault = readlines(fname)
    contents = Set{Char}()
    ix = 0
    iy = 0

    for (y, row) = enumerate(vault)
        for (x, c) = enumerate(row)
            if c == '@'
                ix = x; iy = y
            elseif c >= 'a' && c <= 'z'
                push!(contents, c)
            end
        end
    end

    return contents, ix, iy, vault
end

function searchvault(vault::Array{String,1}, ix::Int, iy::Int, tocollect::Set{Char}; remdist::Dict{Int,Int} = Dict{Int,Int}())
    if length(tocollect) == 0; return 0 end

    xstack = [(ix, iy, 0)]
    distto = Dict([((ix, iy), 0)])

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    mindistfound = typemax(Int)

    while length(xstack) > 0
        (x, y, dist) = pop!(xstack)
        if dist >= mindistfound; continue end
        for dir = dirs
            nx, ny = x + dir[1], y + dir[2]
            if vault[ny][nx] == '#' || in(vault[ny][nx] + 32, tocollect)
                continue
            end
            if !haskey(distto, (nx, ny)) || distto[(nx, ny)] > dist + 1
                c = vault[ny][nx]
                if c in tocollect
                    remhash = sum([2^(x - 'a') for x in tocollect]) + 2^26 * (c-'a')
                    if !haskey(remdist, remhash)
                        remdist[remhash] = searchvault(vault, nx, ny, setdiff(tocollect, c), remdist = remdist)
                    end
                    if dist + 1 + remdist[remhash] < mindistfound
                        mindistfound = remdist[remhash] + dist + 1
                    end
                end
                push!(xstack, (nx, ny, dist + 1))
                distto[(nx, ny)] = dist + 1
            end
        end
    end

    return mindistfound
end