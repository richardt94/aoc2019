function readvault(fname::String)
    # return set of characters in the vault, initial location and map of vault as list of strings
    vault = readlines(fname)
    contents = Set{Char}()
    istate = Array{NTuple{2,Int},1}()

    for (y, row) = enumerate(vault)
        for (x, c) = enumerate(row)
            if c == '@'
                push!(istate, (x,y))
            elseif c >= 'a' && c <= 'z'
                push!(contents, c)
            end
        end
    end

    return vault, contents, istate
end

function searchvault(vault::Array{String,1}, istate::Array{NTuple{2,Int},1}, tocollect::Set{Char}; remdist::Dict = Dict())
    if length(tocollect) == 0; return 0 end

    mindistfound = typemax(Int)

    for (robotidx, (ix, iy)) = enumerate(istate)
        xstack = [(ix, iy, 0)]
        distto = Dict([((ix, iy), 0)])

        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

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
                        remset = setdiff(tocollect,c)
                        nstate = copy(istate)
                        nstate[robotidx] = (nx, ny)
                        if !haskey(remdist, (remset, nstate))
                            remdist[(remset, nstate)] = searchvault(vault, nstate, remset, remdist = remdist)
                        end
                        if dist + 1 + remdist[(remset, nstate)] < mindistfound
                            mindistfound = remdist[(remset, nstate)] + dist + 1
                        end
                    end
                    push!(xstack, (nx, ny, dist + 1))
                    distto[(nx, ny)] = dist + 1
                end
            end
        end
    end

    return mindistfound
end